#include "esphome.h"

class SpaClimate : public Component, public Climate {
 public:
  SpaClimate(UARTComponent *uart) : uart_(uart) {}

  void setup() override {
    this->mode = CLIMATE_MODE_HEAT;
    this->action = CLIMATE_ACTION_IDLE;
    this->target_temperature = 37.0;
    this->current_temperature = NAN;
  }

  ClimateTraits traits() override {
    auto traits = climate::ClimateTraits();
    traits.set_supports_current_temperature(true);
    traits.set_supported_modes({CLIMATE_MODE_HEAT});
    traits.set_supports_action(true);
    traits.set_visual_min_temperature(26.0);
    traits.set_visual_max_temperature(40.0);
    traits.set_visual_temperature_step(0.5);
    return traits;
  }

  void control(const ClimateCall &call) override {
    if (call.get_target_temperature().has_value()) {
      float temp = *call.get_target_temperature();
      this->target_temperature = temp;

      char cmd[20];
      sprintf(cmd, "CMD:SETTEMP:%.1f\n", temp);
      uart_->write_str(cmd);

      ESP_LOGI("spa_climate", "Setting target temperature to %.1f", temp);
    }
    this->publish_state();
  }

  void set_current_temperature(float temp) {
    this->current_temperature = temp;
    this->publish_state();
  }

  void set_target_temperature(float temp) {
    this->target_temperature = temp;
    this->publish_state();
  }

  void set_heating(bool heating) {
    this->action = heating ? CLIMATE_ACTION_HEATING : CLIMATE_ACTION_IDLE;
    this->publish_state();
  }

 private:
  UARTComponent *uart_;
};
