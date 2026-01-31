import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import CONF_ID, UNIT_MINUTE, ICON_TIMER
from . import gecko_spa_ns, GeckoSpa

DEPENDENCIES = ["gecko_spa"]

CONF_GECKO_SPA_ID = "gecko_spa_id"
CONF_SENSOR_TYPE = "type"

SENSOR_TYPES = {
    "pump_timer": "PUMP_TIMER",
}

CONFIG_SCHEMA = sensor.sensor_schema(
    unit_of_measurement=UNIT_MINUTE,
    icon=ICON_TIMER,
    accuracy_decimals=0,
).extend(
    {
        cv.GenerateID(CONF_GECKO_SPA_ID): cv.use_id(GeckoSpa),
        cv.Required(CONF_SENSOR_TYPE): cv.enum(SENSOR_TYPES, lower=True),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_GECKO_SPA_ID])
    var = await sensor.new_sensor(config)

    sensor_type = config[CONF_SENSOR_TYPE]
    if sensor_type == "pump_timer":
        cg.add(parent.set_pump_timer_sensor(var))
