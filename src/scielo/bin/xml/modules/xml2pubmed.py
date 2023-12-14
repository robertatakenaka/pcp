# coding=utf-8
import os
import sys
import shutil
import Tkinter

from __init__ import _
import utils
import xml_utils
import fs_utils
import java_xml_utils
import article
import dbm_isis
import xc_config


global ucisis


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


def find_xml_files_folders(path, folders=[]):
    for item in os.listdir(path):
        folder = path + '/' + item
        if os.path.isdir(folder):
            xml_files = [f for f in os.listdir(folder) if f.endswith('.xml')]
            if len(xml_files) > 0:
                folders.append(folder)
            folders = find_xml_files_folders(folder, folders)
    return folders


def find_xml_files(filenames, folders):
    files = {}
    for filename in filenames:
        for xml_folder_path in folders:
            if filename in os.listdir(xml_folder_path):
                files[filename] = os.path.join(xml_folder_path, filename)
                break
    return files


def find_xml_files_in_alternative(filenames, main_path, found_files={}):
    for item in os.listdir(main_path):
        if os.path.isfile(main_path + '/' + item):
            if item in filenames:
                if not item in found_files.keys():
                    found_files[item] = main_path + '/' + item

        elif os.path.isdir(main_path + '/' + item):
            found_files = find_xml_files_in_alternative(filenames, main_path + '/' + item, found_files)
    return found_files


def load_articles(filenames):
    files = {}
    for name, f in filenames.items():
        content = fs_utils.read_file(f)
        xmlcontent = xml_utils.XMLContent(content)
        xmlcontent.normalize()
        xml, error = xml_utils.load_xml(xmlcontent.content)
        if xml is not None:
            files[name] = xml_utils.tostring(xml.getroot())
        else:
            print(' ERROR 1: Invalid XML {}'.format(name))
    return files


class InputForm(object):

    def __init__(self, tkFrame, default_path):

        self.tkFrame = tkFrame
        self.selected_xml_folder = None
        self.valid_xml_folder = None
        self.default_path = default_path
        self.issue_path = None
        self.acron = None
        self.issueid = None
        self.from_date = None
        self.selected_issue_folder = None

        if default_path is None:
            self.default_path = CURRENT_PATH

        self.tkFrame.label_frame_xml_folder = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.label_frame_xml_folder.pack(fill="both", expand="yes")

        self.tkFrame.label_frame_issue_folder = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.label_frame_issue_folder.pack(fill="both", expand="yes")

        self.tkFrame.label_frame_message = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.label_frame_message.pack(fill="both", expand="yes")

        self.tkFrame.label_frame_from_date = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.label_frame_from_date.pack(fill="both", expand="yes")

        self.tkFrame.label_frame_buttons = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.label_frame_buttons.pack(fill="both", expand="yes")

        #
        self.tkFrame.label_issue_folder = Tkinter.Label(self.tkFrame.label_frame_issue_folder, text=_('issue folder (located in serial folder):'), font="Verdana 12 bold")
        self.tkFrame.label_issue_folder.pack(side='left')
        self.tkFrame.input_issue_folder = Tkinter.Label(self.tkFrame.label_frame_issue_folder, width=50, bd=1, bg='gray')
        self.tkFrame.input_issue_folder.pack(side='left')
        self.tkFrame.button_choose_issue_folder = Tkinter.Button(self.tkFrame.label_frame_issue_folder, text=_('choose folder'), command=self.select_issue_folder)
        self.tkFrame.button_choose_issue_folder.pack()

        self.tkFrame.label_from_date = Tkinter.Label(self.tkFrame.label_frame_from_date, text=_('from date'))
        self.tkFrame.label_from_date.pack(side='left')
        self.tkFrame.input_from_date = Tkinter.Entry(self.tkFrame.label_frame_from_date, bd=5)
        self.tkFrame.input_from_date.pack(side='right')

        self.tkFrame.label_message = Tkinter.Label(self.tkFrame.label_frame_message)
        self.tkFrame.label_message.pack()

        self.tkFrame.button_ok = Tkinter.Button(self.tkFrame.label_frame_buttons, text=_('ok'), command=self.ok)
        self.tkFrame.button_ok.pack(side='right')

        self.tkFrame.button_cancel = Tkinter.Button(self.tkFrame.label_frame_buttons, text=_('cancel'), command=self.cancel)
        self.tkFrame.button_cancel.pack(side='right')

        #self.collection_name = None

    def select_issue_folder(self):
        from tkFileDialog import askdirectory
        if self.selected_issue_folder is not None:
            self.default_path = self.selected_issue_folder
        self.selected_issue_folder = askdirectory(parent=self.tkFrame, initialdir=self.default_path, title=_('Select the issue folder'))
        self.tkFrame.input_issue_folder.config(text=self.selected_issue_folder)
        if self.selected_issue_folder is None:
            self.selected_issue_folder = ''
        else:
            self.display_message(self.selected_issue_folder, '#EAFDE6')

    def display_message(self, msg, color):
        if len(msg) > 0:
            self.tkFrame.label_message.config(text=msg, bg=color)
            self.tkFrame.label_message.update_idletasks()

    def validate_issue_folder(self):
        if self.selected_issue_folder != '':
            if os.path.isdir(self.selected_issue_folder):
                if '/serial/' in self.selected_issue_folder.lower():
                    path = self.selected_issue_folder[self.selected_issue_folder.find('/serial/') + len('/serial/'):]
                    folders = path.split('/')
                    if len(folders) == 2:
                        self.issue_path = self.selected_issue_folder

    def ok(self):
        self.validate_issue_folder()
        self.from_date = self.tkFrame.input_from_date.get()
        if self.issue_path is None:
            self.display_message(_('Select the issue folder (serial/<acron>/<issue number>).'), '#CE3B67')
        else:
            self.tkFrame.quit()

    def cancel(self):
        self.issue_path = None
        self.tkFrame.quit()


class IssueStuff(object):

    def __init__(self, ucisis, issue_path, from_date, final_date):
        self.ucisis = ucisis
        self.issue_path = issue_path
        self.serial_path = os.path.dirname(os.path.dirname(issue_path))
        folders = issue_path.split('/')
        self.acron = folders[-2]
        self.issueid = folders[-1]
        self.pubmed_path = issue_path + '/PubMed'
        if not os.path.isdir(self.pubmed_path):
            os.makedirs(self.pubmed_path)
        self.temp_path = issue_path + '/TMP'
        if not os.path.isdir(self.temp_path):
            os.makedirs(self.temp_path)
        self.articles_db_filename = issue_path + '/base/' + self.issueid
        self.from_date = from_date
        self.final_date = final_date
        self.tmp_db_filename = self.temp_path + '/pubmed_tmp_' + self.issueid
        self.pubmed_folder_in_serial = self.serial_path + '/PubMed'
        self.pubmed_folder_in_acron = self.serial_path + '/' + self.acron + '/PubMed'
        shutil.copyfile(self.articles_db_filename + '.mst', self.tmp_db_filename + '.mst')
        shutil.copyfile(self.articles_db_filename + '.xrf', self.tmp_db_filename + '.xrf')
        self._articles_meta = None
        self._articles_files = None

    @property
    def articles_metadata(self):
        if self._articles_meta is None:
            self._articles_meta = ArticlesDB(self.ucisis, self.tmp_db_filename).articles(self.from_date, self.final_date)
        return self._articles_meta

    @property
    def articles_files(self):
        if self._articles_files is None:
            if self.articles_metadata is not None:
                self._articles_files = ArticlesFiles(self.issue_path, self.articles_metadata)
        return self._articles_files


class ArticlesDB(object):

    def __init__(self, ucisis, db_filename):

        self.isis_db = None
        if os.path.isfile(db_filename + '.mst'):
            self.isis_db = dbm_isis.IsisDB(ucisis, db_filename, CURRENT_PATH + '/articles.fst')
            self.isis_db.update_indexes()
        else:
            print('Not found: ' + db_filename)

    def articles(self, from_date=None, final_date=None):
        items = {}
        int_from_date = 0
        int_final_date = int(utils.now()[0])

        if from_date is not None:
            if from_date != '':
                int_from_date = int(from_date)
        if final_date is not None:
            if final_date != '':
                int_final_date = int(final_date)
        if self.isis_db is not None:
            h_records = self.isis_db.get_records('tp=i or tp=h')
            #h_records = [record for record in h_records if record.get('706') in 'ih']

            issn_id = h_records[0].get('35')
            pid = '0'*4 + h_records[0].get('36')[4:]
            issue_pid = h_records[0].get('36')[:4] + pid[-4:]

            unmatched = []
            matched = []

            for item in h_records:
                if item.get('706') == 'o':
                    a_date = int(item.get('91'))
                elif item.get('706') == 'h':
                    a_date = int(item.get('223', 0))
                    if int_from_date <= a_date <= int_final_date:
                        a_pid = '0'*5 + item.get('121')
                        items[os.path.basename(item.get('702'))] = 'S' + issn_id + issue_pid + a_pid[-5:]
                        matched.append(a_date)
                    else:
                        unmatched.append(a_date)

            if len(matched) > 0:
                print(str(len(matched)) + ' items')
        return items


class ArticlesFiles(object):

    def __init__(self, issue_path, selected_pids):
        self.issue_path = issue_path
        self.selected_pids = selected_pids

    @property
    def selected_articles(self):
        found = find_xml_files(self.selected_pids.keys(), self.standard_xml_folder_paths)
        if len(found) < len(self.selected_pids.keys()):
            failed = [item for item in self.selected_pids.keys() if not item in found.keys()]
            found = find_xml_files_in_alternative(failed, self.issue_path, found)
            failed = [item for item in failed if not item in found.keys()]

            if len(failed) > 0:
                print('Not found: ')
                print('\n'.join(failed))
        return load_articles(found)

    @property
    def standard_xml_folder_paths(self):
        xml_path_list = []
        for path in [self.issue_path + '/base_xml/base_source', self.issue_path + '/markup_xml/scielo_package']:
            if os.path.isdir(path):
                if len([item for item in os.listdir(path) if item.endswith('.xml')]) > 0:
                    xml_path_list.append(path)
        return xml_path_list


class PubMedXMLMaker(object):

    def __init__(self, issue_stuff, xsl_filename):
        self.issue_stuff = issue_stuff
        self.xsl_filename = xsl_filename
        self.debug = False

    @property
    def pubmed_filename(self):
        suffix = '' if self.issue_stuff.from_date is None else self.issue_stuff.from_date + '-' + self.issue_stuff.final_date
        return os.path.join(self.issue_stuff.pubmed_path, self.issue_stuff.acron + self.issue_stuff.issueid + suffix + '.xml')

    @property
    def temp_xml_filename(self):
        temp_filename = self.issue_stuff.temp_path + '/pubmed_tmp_' + os.path.basename(self.pubmed_filename)
        xml_content = '<?xml version="1.0" encoding="utf-8"?>\n'
        xml_content += '<root>'
        xml_content += self.articles_filenames_xml_content
        xml_content += self.articles_pids_xml_content
        xml_content += '</root>'
        fs_utils.write_file(temp_filename, xml_content)
        return temp_filename

    @property
    def articles_filenames_xml_content(self):
        return '<article-set>' + ''.join(['<article-item filename="' + filename + '">' + item + '</article-item>' for filename, item in self.issue_stuff.articles_files.selected_articles.items()]) + '</article-set>'

    @property
    def articles_pids_xml_content(self):
        return '<pid-set>' + ''.join(['<pid filename="' + k + '">' + v + '</pid>' for k, v in sorted(self.issue_stuff.articles_files.selected_pids.items())]) + '</pid-set>'

    def execute_procedures(self):
        self.build_pubmed_xml()

        #if os.path.isfile(self.pubmed_filename):
        #    import webbrowser
        #    webbrowser.open('file:///' + self.pubmed_filename.replace('\\', '/'), new=2)
        #    print(self.pubmed_filename)

        valid = self.validate_pubmed_xml()
        if valid:
            shutil.copyfile(self.pubmed_filename, self.issue_stuff.pubmed_folder_in_acron + '/' + os.path.basename(self.pubmed_filename))
            shutil.copyfile(self.pubmed_filename, self.issue_stuff.pubmed_folder_in_serial + '/' + os.path.basename(self.pubmed_filename))

        if self.debug is False and valid:
            self.clean_temporary_files()
        # validate
        # envia ftp

    def build_pubmed_xml(self):
        java_xml_utils.xml_transform(self.temp_xml_filename, self.xsl_filename, self.pubmed_filename)

    def validate_pubmed_xml(self):
        r = False
        if java_xml_utils.xml_validate(self.pubmed_filename, self.pubmed_filename + '.err'):
            os.unlink(self.pubmed_filename + '.err')
            r = True
            print('Validates fine')
        else:
            print('Validation error: ' + self.pubmed_filename + '.err')
        return r

    def clean_temporary_files(self):
        for item in os.listdir(self.issue_stuff.temp_path):
            if item.startswith('pubmed_'):
                os.unlink(self.issue_stuff.temp_path + '/' + item)


def call_execute_pubmed_procedures(args):

    script, issue_path, from_date, final_date, debug = read_inputs(args)

    if issue_path is None:
        # GUI
        issue_path, from_date = read_form_inputs()
        script = 'exit'
        final_date = utils.now()[0]
        debug = False

    errors = []
    if issue_path is None and script != 'exit':
        errors.append('ERROR: ' + _('Incorrect parameters'))
        errors.append('\n' + _('Usage') + ':')
        errors.append('python ' + script + ' <issue_path>')
        errors.append(_('where') + ':')
        errors.append('  <issue_path> = ' + _('issue folder in serial folder'))

    if not os.path.isdir(issue_path):
        errors.append(_('issue path is not a folder'))

    if len(errors) == 0:
        config = xc_config.XMLConverterConfiguration(CURRENT_PATH + '/../../scielo_paths.ini')
        ucisis = dbm_isis.UCISIS(dbm_isis.CISIS(config.cisis1030), dbm_isis.CISIS(config.cisis1660))

        if ucisis.is_available:
            issue_stuff = IssueStuff(ucisis, issue_path, from_date, final_date)

            pubmed_xml_maker = PubMedXMLMaker(issue_stuff, CURRENT_PATH + '/../../pmc/v3.0/xsl/xml2pubmed/xml2pubmed.xsl')
            pubmed_xml_maker.debug = debug
            pubmed_xml_maker.execute_procedures()
        else:
            errors.append(_('cisis expected'))

    if len(errors) > 0:
        utils.display_message('\n'.join(errors))


def read_inputs(args):
    args = [arg.decode(encoding=sys.getfilesystemencoding()).replace('\\', '/') for arg in args]
    script = None
    issue_path = None
    from_date = None
    final_date = None
    debug = False
    if '--debug' in args:
        debug = True
        args = [item for item in args if item != '--debug']
    if len(args) == 2:
        script, issue_path = args
    elif len(args) == 3:
        script, issue_path, from_date = args
    elif len(args) == 4:
        script, issue_path, from_date, final_date = args
    return (script, issue_path, from_date, final_date, debug)


def read_form_inputs(default_path=None):
    tk_root = Tkinter.Tk()
    tk_root.title('XML 2 PubMed')

    tkFrame = Tkinter.Frame(tk_root)

    form = InputForm(tkFrame, default_path)
    form.tkFrame.pack(side="top", fill="both", expand=True)

    tk_root.mainloop()
    tk_root.focus_set()
    return (form.issue_path, form.from_date)

