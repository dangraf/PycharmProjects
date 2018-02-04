from mongoengine import Document, StringField, ListField


class SettingsList(Document):
    name = StringField(unique=True, required=True)
    list = ListField(StringField())
    meta = {
        'db_alias': 'settings',
        'collection': 'lists'
    }


def get_settingslist(listname: str) -> SettingsList:
    """
    Finds a list in the settings collection
    :param listname: name of the list to be found
    :return: returns a SettingsList object
    """
    setlist = SettingsList.objects(name=listname).first()
    return setlist


def get_safe_settingslist(name: str, defaultlist) -> SettingsList:
    """
    tries to get a list from database. If it does not exist, it creates it by the
    default settings. If no connection could be made by database, the default list
    is returned.

    :param name:   name of list, see "get_Settingslist"
    :param defaultlist: list of strings that is contained in the list.
    :return: Settingslist object
    """
    settings_list = get_settingslist(name)

    # initate list if does not exist
    if settings_list is None:
        settings_list = SettingsList()
        settings_list.name = name
        settings_list.list = defaultlist

        try:
            settings_list.save()
        except BaseException as e:
            print(e)
            pass
    return settings_list
