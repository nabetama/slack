# coding: utf-8

from __future__ import absolute_import, division
import json
import re
import datetime
import dateutil.parser
import dateutil.tz
import six


_url_to_api_object = {}


class FromUrl(object):
    def __init__(self, url, _requests):
        self.url = url
        self._requests = _requests or __import__('requests')

    def __call__(self, **kwargs):
        for regix, klass in six.iteritems(_url_to_api_object):
            if regix.match(self.url):
                return klass(self, **kwargs)  # 自分自身を渡す
        raise NotImplementedError

    def get(self, **kwargs):
        self._requests.get(self.url, data=kwargs)

    def __repr__(self):
        return "<%s url=%r>" % (type(self).__name__, self.url)


class RestObject(object):
    def __init__(self, from_url, **kwargs):
        self.url = from_url.url
        self._requests = from_url._requests
        self.params = kwargs.copy()

    # TODO: self._requests.request のGET, POSTをここでラップしたい


# ================================================================================================
# Api
# ================================================================================================
class Api(RestObject):
    @property
    def test(self):
        return FromUrl('https://slack.com/api/api.test', self._requests)()
_url_to_api_object[re.compile(r'^https://slack.com/api$')] = Api


class ApiTest(RestObject):
    def get(self, **kwargs):
        params = kwargs.copy()
        return self._requests.get(self.url, data=params)
_url_to_api_object[re.compile(r'^https://slack.com/api/api.test$')] = ApiTest


# ================================================================================================
# Auth
# ================================================================================================
class Auth(RestObject):
    @property
    def test(self):
        return FromUrl('https://slack.com/api/auth.test', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/auth$')] = Auth


class AuthTest(RestObject):
    def post(self, **kwargs):
        return self._requests.request('POST', self.url, data=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/auth.test$')] = AuthTest

# ================================================================================================
# Channels
# ================================================================================================
class Channels(RestObject):
    @property
    def list(self):
        return FromUrl('https://slack.com/api/channels.list', self._requests)(data=self.params)

    def archive(self, channel):
        if not channel:
            print '[DEBUG] Input archive channel id.'
        self.params.update({'channel': channel})
        return FromUrl('https://slack.com/api/channels.archive', self._requests)(data=self.params)

    def create(self, name):
        if not name:
            print '[DEBUG] Input name for new channel.'
        self.params.update({'name': name})
        return FromUrl('https://slack.com/api/channels.create', self._requests)(data=self.params)

    def history(self, channel, **kwargs):
        """ https://api.slack.com/methods/channels.history
        latest, oldest, count
        """
        if not channel:
            print '[DEBUG] Please input the channel you\'d like to see.'
        self.params.update({'channel': channel})
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/channels.history', self._requests)(data=self.params)

    def info(self, channel):
        self.params.update({'channel': channel})
        return FromUrl('https://slack.com/api/channels.info', self._requests)(data=self.params)

    def invite(self, channel, user):
        self.params.update({
            'channel':  channel,
            'user':     user,
            })
        return FromUrl('https://slack.com/api/channels.invite', self._requests)(data=self.params)

    def join(self, channel):
        """ https://api.slack.com/methods/channels.join
        """
        self.params.update({
            'name': channel,
            })
        return FromUrl('https://slack.com/api/channels.join', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/channels$')] = Channels


class ChannelArchive(RestObject):
    def post(self, **kwargs):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.archive$')] = ChannelArchive


class ChannelCreate(RestObject):
    def post(self, **kwargs):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.create$')] = ChannelCreate


class ChannelHistory(RestObject):
    def get(self, **kwargs):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.history$')] = ChannelHistory


class ChannelInfo(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.info$')] = ChannelInfo


class ChannelInvite(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.invite$')] = ChannelInvite


class ChannelJoin(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.join$')] = ChannelJoin


class ChannelList(RestObject):
    def get(self, **kwargs):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.list$')] = ChannelList

