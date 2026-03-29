from __future__ import print_function

import re
from inspect import isclass

import six


try:
    bool(type(unicode))
except NameError:
    unicode = str


def isconfig(obj):
    return isclass(obj) and issubclass(obj, Config)


def all_vars(obj):
    return {k: getattr(obj, k) for k in dir(obj) if k[0] != "_" and getattr(obj, k) != "{!IGNORE}"}


class Config(object):
    raise_on_error = False

    @classmethod
    def process_references(cls):
        unknown_values = []

        cls.detect_unknown(unknown_values, "")
        unknown_values.reverse()

        anything_changed = True
        while unknown_values and anything_changed:
            anything_changed = False
            for config, param_name, param_value in unknown_values[:]:
                assert isconfig(config)
                success = config.set_value(cls, param_name, param_value)
                if success:
                    unknown_values.remove((config, param_name, param_value))
                    anything_changed = True

        if cls.raise_on_error and unknown_values:
            errors = ", ".join("{} ({})".format(param, value) for _, param, value in unknown_values)
            raise Exception("Cannot resolve config params: " + errors)

        for config, param_name, param_value in unknown_values:
            print("Warning: Cannot resolve config param '{}'. Value: '{}'".format(param_name, param_value))
            setattr(config, param_name, param_value)

    @classmethod
    def detect_unknown(cls, unknown_values, path):
        if cls.__name__ != "config":
            if path: path += "."
            path += cls.__name__
        for subclass in cls.mro():
            if not isconfig(subclass): continue
            for param_name, param_value in six.iteritems(all_vars(subclass).copy()):
                if param_name[0] == '_': continue
                if isconfig(param_value):
                    param_value.detect_unknown(unknown_values, path)
                elif isinstance(param_value, six.string_types) and '{' in param_value and '}' in param_value:
                    # for ref in re.findall(r"{\w+?}", param_value):
                    #     if "{" + ref + "}" in param_value: continue
                    #     newref = "{" + path + "." + ref[1:]
                    #     param_value = param_value.replace(ref, newref)
                    unknown_values.append((subclass, param_name, param_value))

    @classmethod
    def set_value(cls, main_config, param_name, param_value):
        try:
            values = all_vars(main_config)
            values.update(all_vars(cls))
            val = param_value.format(**values)
            setattr(cls, param_name, val)
            return True
        except Exception:
            return False

    @classmethod
    def asdict(cls, *args):
        if len(args) == 1:  # zeby bylo kompatybilne wstecznie (wczesniej byla to funkcja statyczna...)
            cls = args[0]
        d = all_vars(cls)
        d = {k:v for k,v in six.iteritems(d) if k not in ("asdict", "detect_unknown", "process_references", "set_value", "raise_on_error", "apply_config")}
        for param_name, param_value in six.iteritems(d):
            if isconfig(param_value):
                d[param_name] = param_value.asdict()
        return d

    @classmethod
    def apply_config(old_config, new_config):
        # print "Applying config {} to {}".format(new_config, old_config)
        vars_new = vars(new_config)
        for param_name, param_value in six.iteritems(vars_new):
            if param_name[0] == '_': continue
            if isconfig(param_value) and hasattr(old_config, param_name):
                getattr(old_config, param_name).apply_config(param_value)
            else:
                setattr(old_config, param_name, param_value)


def apply_config(new_config):
    main_config = new_config.mro()[-3]
    main_config.apply_config(new_config)
    return main_config


def asdict(config):
    return config.asdict()


__all__ = ["Config", "apply_config", "asdict"]

