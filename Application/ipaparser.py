import os
import re
import tempfile
import biplist

#######
# ipin decode png
# zip unzip ipa
#
#


__author__ = 'ryan'

from zipfile import ZipFile
import ipin


class IPAParser:

    def __init__(self, ipa_path):
        self.ipa_path = ipa_path
        self.ipa = ZipFile(self.ipa_path, 'r')
        self.info_plist = self.find_info_plist()
        # self.ipa.close()

    def __del__(self):
        self.ipa.close()

    def find_info_plist(self):
        temp_folder = tempfile.gettempdir()
        name_list = self.ipa.namelist()
        re_info = re.compile(r"^Payload/[^/]+.app/Info.plist$", re.IGNORECASE)
        for name in name_list:
            match = re_info.match(name)
            if match:
                info_path = name
                break
        if info_path is None:
            return None
        real_info_path = self.ipa.extract(info_path, temp_folder)
        plist = biplist.readPlist(real_info_path)

        return plist

    def bundle_identifier(self):
        bundle_identifier = self.info_plist.get("CFBundleIdentifier", None)
        return bundle_identifier

    def bundle_name(self):
        bundle_name =  self.info_plist.get(r'CFBundleName', None)
        return bundle_name

    def version(self):
        bundle_version = self.info_plist.get(r'CFBundleVersion', None)
        return bundle_version

    def bundle_short_version(self):
        bundle_short_version = self.info_plist.get(r'CFBundleVersion', None)
        return bundle_short_version

    def icon_file_names(self):
        icons = self.info_plist.get(r'CFBundleIcons', None)
        icons_file_names = []
        if len(icons) > 0:
            icons_file_names = icons.get(r"CFBundlePrimaryIcon", None).get(r"CFBundleIconFiles", None)
        else:
            icons = self.info_plist.get(r"CFBundleIconFiles", None)
            if icons:
                icons_file_names = icons

        return icons_file_names

    def icons(self):
        matched_entries = []
        icons_file_names = self.icon_file_names()
        name_list = self.ipa.namelist()
        temp_folder = tempfile.gettempdir()

        for name in name_list:
            for icon_name in icons_file_names:
                re_string = r"Payload\/(.)*\.app\/" + icon_name + r"(.)*.png"
                re_info = re.compile(re_string, re.IGNORECASE)

                if re_info.match(name):
                    matched_entries.append(self.ipa.extract(name, path=temp_folder))

        return matched_entries

    def crushed_icon(self):
        return self.icons()[-1]

    def icon(self):
        crushed_icon = self.crushed_icon()
        if crushed_icon:
            ipin.updatePNG(crushed_icon)
        return crushed_icon


if __name__ == '__main__':
    ipa_parser = IPAParser("/Users/ryan/Desktop/EMStock0515.ipa")
    # print(ipa_parser.icon_file_names())
    # print(ipa_parser.icons())
    print(ipa_parser.icon())
