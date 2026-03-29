from vision.config.config import Config, apply_config


class config(Config):
    pass


def auto_config(new_config):
    config.apply_config(new_config)
    config.process_references()
    return new_config


