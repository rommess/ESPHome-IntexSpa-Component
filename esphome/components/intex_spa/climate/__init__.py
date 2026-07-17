import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate
from .. import intex_spa_ns, IntexSpa, CONF_INTEX_SPA_ID

SpaClimate = intex_spa_ns.class_("SpaClimate", climate.Climate, cg.Component)

# climate_schema() is the current API (replaces the deprecated CLIMATE_SCHEMA).
# We extend it with our hub reference.
CONFIG_SCHEMA = climate.climate_schema(SpaClimate).extend(
    {
        cv.GenerateID(CONF_INTEX_SPA_ID): cv.use_id(IntexSpa),
    }
)


async def to_code(config):
    # new_climate() instantiates the C++ object and registers it; replaces
    # the old cg.new_Pvariable + register_climate pattern.
    var = await climate.new_climate(config)
    await cg.register_component(var, config)
    await cg.register_parented(var, await cg.get_variable(config[CONF_INTEX_SPA_ID]))
    hub = await cg.get_variable(config[CONF_INTEX_SPA_ID])
    cg.add(hub.set_climate(var))
