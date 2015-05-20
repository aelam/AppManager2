#!/usr/bin/env python
#coding=utf-8
#

from django.db import models
from django.core.files.uploadedfile import TemporaryUploadedFile
from zipfile import ZipFile
from AppManager import settings
import re, os, tempfile, biplist, shutil, uuid, datetime, plistlib
from django.contrib.auth.models import User
from ipaparser import IPAParser

PLIST_START_MARKER = '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
PLIST_END_MARKER = '</plist>'



class ProvisioningProfile(models.Model):
    profile_path = models.FileField(upload_to="profiles")

    applicationIdentifierPrefix = models.CharField(max_length=100, editable=False)
    create_at = models.DateTimeField(editable=False, auto_now_add=True, blank=True)
    application_identifier = models.CharField(max_length=100, editable=False, null=True)
    name = models.CharField(max_length=100, editable=False, null=True)
    provisionsAllDevices = models.BooleanField(default=False, editable=False)
    expirationDate = models.DateTimeField(editable=False, null=True)
    UUID = models.CharField(max_length=100, editable=False, null=True)

    PROFILE_TYPE_CHOICES = (
        ("DEBUG", "debug"),
        ("AD-HOC", "ad-hoc"),
        ("APPSTORE", "appstore"),
    )
    profile_type = models.CharField(max_length=100, choices=PROFILE_TYPE_CHOICES, default="DEBUG")


    def ProfileToPlist(profile_path):
    # print(profile_path)
        with open(profile_path, "rb") as provisioning_file:
            file_contents = provisioning_file.read()

        plist_start = file_contents.find(PLIST_START_MARKER)
        plist_end = file_contents.find(PLIST_END_MARKER)
        if plist_start < 0 or plist_end < 0:
            return None

        plist_end += len(PLIST_END_MARKER)

        plist_dict = plistlib.readPlistFromString(file_contents[plist_start:plist_end])

        # print(plist_dict)
        print plist_dict["DeveloperCertificates"]
        return plist_dict

class App(models.Model):
    app_identifier = models.CharField(max_length=60, unique=True)
    app_name = models.CharField(max_length=60)
    app_store_id = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.app_name


class Package(models.Model):
    app = models.ForeignKey(App)

    create_at = models.DateTimeField(auto_now_add=True)
    ipa_path = models.FileField(upload_to='apps/')

    bundle_identifier = models.CharField(max_length=60, blank=True, null=True)

    bundle_name = models.CharField(max_length=100, blank=True, null=True)
    bundle_version = models.CharField(max_length=100, blank=True, null=True)
    bundle_short_version = models.CharField(max_length=100, blank=True, null=True)

    icon_path = models.FileField(upload_to='apps/icons', editable=False, null=True)
    big_icon_path = models.FileField(upload_to='apps/icons', editable=False, null=True)

    release_note = models.TextField(null=True, blank=True)

    provision = models.ForeignKey(ProvisioningProfile, null=True, blank=True)

    def __unicode__(self):
        return "%s-%s " % (self.bundle_identifier, self.bundle_version)

    class Meta:
        ordering = ['-create_at', 'bundle_short_version']

    def install_link(self):
        return None

    def parse_ipa(self):
        if self.ipa_path is None:
            return None
        ipa_parser = IPAParser(self.ipa_path)
        self.bundle_identifier = ipa_parser.bundle_identifier()
        self.bundle_version = ipa_parser.version()
        self.bundle_short_version = ipa_parser.bundle_short_version()
        self.bundle_name = ipa_parser.bundle_name()

        # copy icon to media path
        icon = ipa_parser.icon()
        dst_dir = os.path.join(settings.MEDIA_ROOT, "apps/icons")
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        random_str = str(uuid.uuid4())
        source_icon_name = random_str + ".png"
        media_dst_path = os.path.join(dst_dir, source_icon_name)
        shutil.copy2(icon, media_dst_path)
        self.icon_path = os.path.join("apps/icons", source_icon_name)
        self.big_icon_path = self.icon_path

        return self.bundle_identifier


class Comment(models.Model):
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    package = models.ForeignKey(Package)

    def __unicode__(self):
        return self.content


class Device(models.Model):
    device_id = models.CharField(max_length=100,unique=True)
    nick = models.CharField(max_length=100,blank=True)


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    team_token = models.CharField(max_length=100)
    owner = models.ForeignKey(User)



