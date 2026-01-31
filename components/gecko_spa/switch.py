import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID
from . import gecko_spa_ns, GeckoSpa

DEPENDENCIES = ["gecko_spa"]

GeckoSpaSwitch = gecko_spa_ns.class_("GeckoSpaSwitch", switch.Switch, cg.Component)

CONF_GECKO_SPA_ID = "gecko_spa_id"
CONF_SWITCH_TYPE = "type"

SWITCH_TYPES = {
    "light": "light",
    "circulation": "circulation",
    "pump1": "pump1",
    "pump2": "pump2",
    "pump3": "pump3",
    "pump4": "pump4",
}

CONFIG_SCHEMA = switch.switch_schema(GeckoSpaSwitch).extend(
    {
        cv.GenerateID(CONF_GECKO_SPA_ID): cv.use_id(GeckoSpa),
        cv.Required(CONF_SWITCH_TYPE): cv.enum(SWITCH_TYPES, lower=True),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_GECKO_SPA_ID])
    var = await switch.new_switch(config)
    await cg.register_component(var, config)

    cg.add(var.set_parent(parent))
    cg.add(var.set_switch_type(config[CONF_SWITCH_TYPE]))

    switch_type = config[CONF_SWITCH_TYPE]
    if switch_type == "light":
        cg.add(parent.set_light_switch(var))
    elif switch_type == "circulation":
        cg.add(parent.set_circ_switch(var))
    elif switch_type == "pump1":
        cg.add(parent.set_pump1_switch(var))
    elif switch_type == "pump2":
        cg.add(parent.set_pump2_switch(var))
    elif switch_type == "pump3":
        cg.add(parent.set_pump3_switch(var))
    elif switch_type == "pump4":
        cg.add(parent.set_pump4_switch(var))
