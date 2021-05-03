import streamlit as st
import json

# the location of the config relative to the workingdir of python
CONFIG_PATH = "./config.json"

def load_config():
    with open(CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)
    return config

def write_config(config):
    with open(CONFIG_PATH, "w") as config_file:
        json.dump(config, config_file, indent=4)

def get_value(name):
    config = load_config()
    try:
        return config[name]["value"]
    except KeyError() as e:
        print(e)

def app():
    config = load_config()
    st.title('Settings')

    # dynamicly create the config page from the config file
    for k, v in config.items():
        st.header(v["name"])
        ui_type = v["type"]

        if ui_type == "text_input":
            v["value"] = st.text_input("", v["value"])

        elif ui_type == "selectbox":
            # TODO bug where you have to select the new value 2 times if you change it multiple times
            options = v["options"]
            index = options.index(v["value"])
            v["value"] = st.selectbox("", options, index=index)

        elif ui_type == "checkbox":
            v["value"] = st.checkbox("", value=v["value"])

    write_config(config)


