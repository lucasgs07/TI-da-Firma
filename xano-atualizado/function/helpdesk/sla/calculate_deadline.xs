function "helpdesk/sla/calculate_deadline" {
  input {
    timestamp start_at
    int sla_horas
  }

  stack {
    precondition ($input.sla_horas >= 1 && $input.sla_horas <= 50) {
      error_type = "inputerror"
      error = "SLA hours must be between 1 and 50."
    }
  
    var $cursor {
      value = $input.start_at
    }
  
    var $remaining_ms {
      value = `$input.sla_horas * 3600000`
    }
  
    var $sla_inicio_em {
      value = null
    }
  
    var $prazo_sla {
      value = null
    }
  
    var $local_date {
      value = ""
    }
  
    var $month_day {
      value = ""
    }
  
    var $weekday {
      value = 0
    }
  
    var $is_holiday {
      value = false
    }
  
    var $is_workday {
      value = false
    }
  
    var $today_start {
      value = 0
    }
  
    var $next_day_start {
      value = 0
    }
  
    var $available_ms {
      value = 0
    }
  
    foreach ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]) {
      each as $day {
        conditional {
          if ($remaining_ms > 0) {
            var.update $local_date {
              value = $cursor|format_timestamp:"Y-m-d":"America/Sao_Paulo"
            }
          
            var.update $month_day {
              value = $cursor|format_timestamp:"m-d":"America/Sao_Paulo"
            }
          
            var.update $weekday {
              value = ($cursor|format_timestamp:"N":"America/Sao_Paulo")|to_int
            }
          
            var.update $is_holiday {
              value = $month_day == "01-01" || $month_day == "04-21" || $month_day == "05-01" || $month_day == "09-07" || $month_day == "10-12" || $month_day == "11-02" || $month_day == "11-15" || $month_day == "11-20" || $month_day == "12-25"
            }
          
            var.update $is_workday {
              value = $weekday >= 1 && $weekday <= 5 && !$is_holiday
            }
          
            var.update $today_start {
              value = ($local_date|concat:" 00:00:00":"")|parse_timestamp:"Y-m-d H:i:s":"America/Sao_Paulo"
            }
          
            var.update $next_day_start {
              value = $today_start|transform_timestamp:"tomorrow":"America/Sao_Paulo"
            }
          
            conditional {
              if ($is_workday) {
                conditional {
                  if ($sla_inicio_em == null) {
                    var.update $sla_inicio_em {
                      value = $cursor
                    }
                  }
                }
              
                var.update $available_ms {
                  value = `$next_day_start - $cursor`
                }
              
                conditional {
                  if ($remaining_ms <= $available_ms) {
                    var.update $prazo_sla {
                      value = $cursor|add:$remaining_ms
                    }
                  
                    var.update $remaining_ms {
                      value = 0
                    }
                  }
                
                  else {
                    var.update $remaining_ms {
                      value = `$remaining_ms - $available_ms`
                    }
                  
                    var.update $cursor {
                      value = $next_day_start
                    }
                  }
                }
              }
            
              else {
                var.update $cursor {
                  value = $next_day_start
                }
              }
            }
          }
        }
      }
    }
  
    precondition ($remaining_ms == 0 && $sla_inicio_em != null && $prazo_sla != null) {
      error = "The SLA deadline could not be calculated within the supported calendar window."
    }
  }

  response = {
    sla_inicio_em: $sla_inicio_em
    prazo_sla    : $prazo_sla
  }
  guid = "ini5OEJea4-MboZBrR5abop6MbI"
}
