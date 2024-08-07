import struct


class PacketHeader:
    def __init__(self, data):
        # if len(data) != 29:
        #     raise ValueError("Invalid data length. Expected 29 bytes.")

        # Unpack the raw data according to the structure format
        self.packet_format = int.from_bytes(data[0:2], byteorder='little')
        self.game_year = int.from_bytes(data[2:3], byteorder='little')
        self.game_major_version = int.from_bytes(data[3:4], byteorder='little')
        self.game_minor_version = int.from_bytes(data[4:5], byteorder='little')
        self.packet_version = int.from_bytes(data[5:6], byteorder='little')
        self.packet_id = int.from_bytes(data[6:7], byteorder='little')
        self.session_uid = int.from_bytes(data[7:15], byteorder='little')
        self.session_time = struct.unpack('<f', data[15:19])[0]
        self.frame_identifier = int.from_bytes(data[19:23], byteorder='little')
        self.overall_frame_identifier = int.from_bytes(data[23:27], byteorder='little')
        self.player_car_index = int.from_bytes(data[27:28], byteorder='little')
        self.secondary_player_car_index = int.from_bytes(data[28:29], byteorder='little')

    def to_dict(self):
        return {
            "packet_format": self.packet_format,
            "game_year": self.game_year,
            "game_major_version": self.game_major_version,
            "game_minor_version": self.game_minor_version,
            "packet_version": self.packet_version,
            "packet_id": self.packet_id,
            "session_uid": self.session_uid,
            "session_time": self.session_time,
            "frame_identifier": self.frame_identifier,
            "overall_frame_identifier": self.overall_frame_identifier,
            "player_car_index": self.player_car_index,
            "secondary_player_car_index": self.secondary_player_car_index
        }


class CarMotionData:
    def __init__(self, data):
        self.world_position_x = struct.unpack('<f', data[0:4])[0]
        self.world_position_y = struct.unpack('<f', data[4:8])[0]
        self.world_position_z = struct.unpack('<f', data[8:12])[0]
        self.world_velocity_x = struct.unpack('<f', data[12:16])[0]
        self.world_velocity_y = struct.unpack('<f', data[16:20])[0]
        self.world_velocity_z = struct.unpack('<f', data[20:24])[0]
        self.world_forward_dir_x = struct.unpack('<h', data[24:26])[0]
        self.world_forward_dir_y = struct.unpack('<h', data[26:28])[0]
        self.world_forward_dir_z = struct.unpack('<h', data[28:30])[0]
        self.world_right_dir_x = struct.unpack('<h', data[30:32])[0]
        self.world_right_dir_y = struct.unpack('<h', data[32:34])[0]
        self.world_right_dir_z = struct.unpack('<h', data[34:36])[0]
        self.g_force_lateral = struct.unpack('<f', data[36:40])[0]
        self.g_force_longitudinal = struct.unpack('<f', data[40:44])[0]
        self.g_force_vertical = struct.unpack('<f', data[44:48])[0]
        self.yaw = struct.unpack('<f', data[48:52])[0]
        self.pitch = struct.unpack('<f', data[52:56])[0]
        self.roll = struct.unpack('<f', data[56:60])[0]

    def to_dict(self):
        return {
            "world_position_x": self.world_position_x,
            "world_position_y": self.world_position_y,
            "world_position_z": self.world_position_z,
            "world_velocity_x": self.world_velocity_x,
            "world_velocity_y": self.world_velocity_y,
            "world_velocity_z": self.world_velocity_z,
            "world_forward_dir_x": self.world_forward_dir_x,
            "world_forward_dir_y": self.world_forward_dir_y,
            "world_forward_dir_z": self.world_forward_dir_z,
            "world_right_dir_x": self.world_right_dir_x,
            "world_right_dir_y": self.world_right_dir_y,
            "world_right_dir_z": self.world_right_dir_z,
            "g_force_lateral": self.g_force_lateral,
            "g_force_longitudinal": self.g_force_longitudinal,
            "g_force_vertical": self.g_force_vertical,
            "yaw": self.yaw,
            "pitch": self.pitch,
            "roll": self.roll
        }


class LapData:
    def __init__(self, data):
        self.last_lap_time_ms = int.from_bytes(data[0:4], byteorder='little')
        self.current_lap_time_ms = int.from_bytes(data[4:8], byteorder='little')
        self.sector1_time_ms = int.from_bytes(data[8:10], byteorder='little')
        self.sector1_time_minutes = int.from_bytes(data[10:11], byteorder='little')
        self.sector2_time_ms = int.from_bytes(data[11:13], byteorder='little')
        self.sector2_time_minutes = int.from_bytes(data[13:14], byteorder='little')
        self.delta_to_car_in_front_ms = int.from_bytes(data[14:16], byteorder='little')
        self.delta_to_race_leader_ms = int.from_bytes(data[16:18], byteorder='little')
        self.lap_distance = struct.unpack('<f', data[18:22])[0]
        self.total_distance = struct.unpack('<f', data[22:26])[0]
        self.safety_car_delta = struct.unpack('<f', data[26:30])[0]
        self.car_position = int.from_bytes(data[30:31], byteorder='little')
        self.current_lap_num = int.from_bytes(data[31:32], byteorder='little')
        self.pit_status = int.from_bytes(data[32:33], byteorder='little')
        self.num_pit_stops = int.from_bytes(data[33:34], byteorder='little')
        self.sector = int.from_bytes(data[34:35], byteorder='little')
        self.current_lap_invalid = int.from_bytes(data[35:36], byteorder='little')
        self.penalties = int.from_bytes(data[36:37], byteorder='little')
        self.total_warnings = int.from_bytes(data[37:38], byteorder='little')
        self.corner_cutting_warnings = int.from_bytes(data[38:39], byteorder='little')
        self.num_unserved_drive_through_pens = int.from_bytes(data[39:40], byteorder='little')
        self.num_unserved_stop_go_pens = int.from_bytes(data[40:41], byteorder='little')
        self.grid_position = int.from_bytes(data[41:42], byteorder='little')
        self.driver_status = int.from_bytes(data[42:43], byteorder='little')
        self.result_status = int.from_bytes(data[43:44], byteorder='little')
        self.pit_lane_timer_active = int.from_bytes(data[44:45], byteorder='little')
        self.pit_lane_time_in_lane_ms = int.from_bytes(data[45:47], byteorder='little')
        self.pit_stop_timer_in_ms = int.from_bytes(data[47:49], byteorder='little')
        self.pit_stop_should_serve_pen = int.from_bytes(data[49:50], byteorder='little')

    def to_dict(self):
        return {
            "last_lap_time_ms": self.last_lap_time_ms,
            "current_lap_time_ms": self.current_lap_time_ms,
            "sector1_time_ms": self.sector1_time_ms,
            "sector1_time_minutes": self.sector1_time_minutes,
            "sector2_time_ms": self.sector2_time_ms,
            "sector2_time_minutes": self.sector2_time_minutes,
            "delta_to_car_in_front_ms": self.delta_to_car_in_front_ms,
            "delta_to_race_leader_ms": self.delta_to_race_leader_ms,
            "lap_distance": self.lap_distance,
            "total_distance": self.total_distance,
            "safety_car_delta": self.safety_car_delta,
            "car_position": self.car_position,
            "current_lap_num": self.current_lap_num,
            "pit_status": self.pit_status,
            "num_pit_stops": self.num_pit_stops,
            "sector": self.sector,
            "current_lap_invalid": self.current_lap_invalid,
            "penalties": self.penalties,
            "total_warnings": self.total_warnings,
            "corner_cutting_warnings": self.corner_cutting_warnings,
            "num_unserved_drive_through_pens": self.num_unserved_drive_through_pens,
            "num_unserved_stop_go_pens": self.num_unserved_stop_go_pens,
            "grid_position": self.grid_position,
            "driver_status": self.driver_status,
            "result_status": self.result_status,
            "pit_lane_timer_active": self.pit_lane_timer_active,
            "pit_lane_time_in_lane_ms": self.pit_lane_time_in_lane_ms,
            "pit_stop_timer_in_ms": self.pit_stop_timer_in_ms,
            "pit_stop_should_serve_pen": self.pit_stop_should_serve_pen
        }


class CarTelemetryData:
    def __init__(self, data):
        self.speed = int.from_bytes(data[0:2], byteorder='little')
        self.throttle = struct.unpack('<f', data[2:6])[0]
        self.steer = struct.unpack('<f', data[6:10])[0]
        self.brake = struct.unpack('<f', data[10:14])[0]
        self.clutch = int.from_bytes(data[14:15], byteorder='little')
        self.gear = int.from_bytes(data[15:16], byteorder='little')
        self.engine_rpm = int.from_bytes(data[16:18], byteorder='little')
        self.drs = int.from_bytes(data[18:19], byteorder='little')
        self.rev_lights_percent = int.from_bytes(data[19:20], byteorder='little')
        self.rev_lights_bit_value = int.from_bytes(data[20:22], byteorder='little')
        self.brakes_temperature = [int.from_bytes(data[i:i + 2], byteorder='little') for i in range(22, 30, 2)]
        self.tyres_surface_temperature = [int.from_bytes(data[i:i + 1], byteorder='little') for i in range(30, 34)]
        self.tyres_inner_temperature = [int.from_bytes(data[i:i + 1], byteorder='little') for i in range(34, 38)]
        self.engine_temperature = int.from_bytes(data[38:40], byteorder='little')
        self.tyres_pressure = [struct.unpack('<f', data[i:i + 4])[0] for i in range(40, 56, 4)]
        self.surface_type = [int.from_bytes(data[i:i + 1], byteorder='little') for i in range(56, 60)]

    def to_dict(self):
        return {
            "speed": self.speed,
            "throttle": self.throttle,
            "steer": self.steer,
            "brake": self.brake,
            "clutch": self.clutch,
            "gear": self.gear,
            "engine_rpm": self.engine_rpm,
            "drs": self.drs,
            "rev_lights_percent": self.rev_lights_percent,
            "rev_lights_bit_value": self.rev_lights_bit_value,
            "brakes_temperature": self.brakes_temperature,
            "tyres_surface_temperature": self.tyres_surface_temperature,
            "tyres_inner_temperature": self.tyres_inner_temperature,
            "engine_temperature": self.engine_temperature,
            "tyres_pressure": self.tyres_pressure,
            "surface_type": self.surface_type
        }


class CarStatusData:
    def __init__(self, data):
        self.traction_control = int.from_bytes(data[0:1], byteorder='little')
        self.anti_lock_brakes = int.from_bytes(data[1:2], byteorder='little')
        self.fuel_mix = int.from_bytes(data[2:3], byteorder='little')
        self.front_brake_bias = int.from_bytes(data[3:4], byteorder='little')
        self.pit_limiter_status = int.from_bytes(data[4:5], byteorder='little')
        self.fuel_in_tank = struct.unpack('<f', data[5:9])[0]
        self.fuel_capacity = struct.unpack('<f', data[9:13])[0]
        self.fuel_remaining_laps = struct.unpack('<f', data[13:17])[0]
        self.max_rpm = int.from_bytes(data[17:19], byteorder='little')
        self.idle_rpm = int.from_bytes(data[19:21], byteorder='little')
        self.max_gears = int.from_bytes(data[21:22], byteorder='little')
        self.drs_allowed = int.from_bytes(data[22:23], byteorder='little')
        self.drs_activation_distance = int.from_bytes(data[23:25], byteorder='little')
        self.actual_tyre_compound = int.from_bytes(data[25:26], byteorder='little')
        self.visual_tyre_compound = int.from_bytes(data[26:27], byteorder='little')
        self.tyres_age_laps = int.from_bytes(data[27:28], byteorder='little')
        self.vehicle_fia_flags = int.from_bytes(data[28:29], byteorder='little')
        self.engine_power_ice = struct.unpack('<f', data[29:33])[0]
        self.engine_power_mguk = struct.unpack('<f', data[33:37])[0]
        self.ers_store_energy = struct.unpack('<f', data[37:41])[0]
        self.ers_deploy_mode = int.from_bytes(data[41:42], byteorder='little')
        self.ers_harvested_this_lap_mguk = struct.unpack('<f', data[42:46])[0]
        self.ers_harvested_this_lap_mguh = struct.unpack('<f', data[46:50])[0]
        self.ers_deployed_this_lap = struct.unpack('<f', data[50:54])[0]
        self.network_paused = int.from_bytes(data[54:55], byteorder='little')

    def to_dict(self):
        return {
            "traction_control": self.traction_control,
            "anti_lock_brakes": self.anti_lock_brakes,
            "fuel_mix": self.fuel_mix,
            "front_brake_bias": self.front_brake_bias,
            "pit_limiter_status": self.pit_limiter_status,
            "fuel_in_tank": self.fuel_in_tank,
            "fuel_capacity": self.fuel_capacity,
            "fuel_remaining_laps": self.fuel_remaining_laps,
            "max_rpm": self.max_rpm,
            "idle_rpm": self.idle_rpm,
            "max_gears": self.max_gears,
            "drs_allowed": self.drs_allowed,
            "drs_activation_distance": self.drs_activation_distance,
            "actual_tyre_compound": self.actual_tyre_compound,
            "visual_tyre_compound": self.visual_tyre_compound,
            "tyres_age_laps": self.tyres_age_laps,
            "vehicle_fia_flags": self.vehicle_fia_flags,
            "engine_power_ice": self.engine_power_ice,
            "engine_power_mguk": self.engine_power_mguk,
            "ers_store_energy": self.ers_store_energy,
            "ers_deploy_mode": self.ers_deploy_mode,
            "ers_harvested_this_lap_mguk": self.ers_harvested_this_lap_mguk,
            "ers_harvested_this_lap_mguh": self.ers_harvested_this_lap_mguh,
            "ers_deployed_this_lap": self.ers_deployed_this_lap,
            "network_paused": self.network_paused
        }


class SessionData:
    def __init__(self, packet_data):
        session_data = packet_data

        # Calculate the offsets for each variable
        weather_offset = 0
        track_temp_offset = weather_offset + 1
        air_temp_offset = track_temp_offset + 1
        laps_offset = air_temp_offset + 1
        track_length_offset = laps_offset + 1
        session_type_offset = track_length_offset + 2
        track_id_offset = session_type_offset + 1
        formula_offset = track_id_offset + 1
        session_time_left_offset = formula_offset + 1
        session_duration_offset = session_time_left_offset + 2
        pit_speed_limit_offset = session_duration_offset + 2
        game_paused_offset = pit_speed_limit_offset + 1
        marshal_zones_offset = game_paused_offset + 1
        safety_car_status_offset = marshal_zones_offset + 21 * 5  # Assuming 5 bytes for MarshalZone

        # Assign values to instance variables using the calculated offsets
        self.weather = int.from_bytes(session_data[weather_offset:weather_offset + 1], byteorder='little')
        self.track_temperature = int.from_bytes(session_data[track_temp_offset:track_temp_offset + 1], byteorder='little')
        self.air_temperature = int.from_bytes(session_data[air_temp_offset:air_temp_offset + 1], byteorder='little')
        self.total_laps = int.from_bytes(session_data[laps_offset:laps_offset + 1], byteorder='little')
        self.track_length = int.from_bytes(session_data[track_length_offset:track_length_offset + 2], byteorder='little')
        self.session_type = int.from_bytes(session_data[session_type_offset:session_type_offset + 1], byteorder='little')
        self.track_id = int.from_bytes(session_data[track_id_offset:track_id_offset + 1], byteorder='little')
        self.formula = int.from_bytes(session_data[formula_offset:formula_offset + 1], byteorder='little')
        self.session_time_left = int.from_bytes(session_data[session_time_left_offset:session_time_left_offset + 2], byteorder='little')
        self.session_duration = int.from_bytes(session_data[session_duration_offset:session_duration_offset + 2], byteorder='little')
        self.pit_speed_limit = int.from_bytes(session_data[pit_speed_limit_offset:pit_speed_limit_offset + 1], byteorder='little')
        self.game_paused = int.from_bytes(session_data[game_paused_offset:game_paused_offset + 1], byteorder='little')
        self.safety_car_status = int.from_bytes(session_data[safety_car_status_offset:safety_car_status_offset + 1], byteorder='little')

    def to_dict(self):
        return {
            "weather": self.weather,
            "track_temperature": self.track_temperature,
            "air_temperature": self.air_temperature,
            "total_laps": self.total_laps,
            "track_length": self.track_length,
            "session_type": self.session_type,
            "track_id": self.track_id,
            "formula": self.formula,
            "session_time_left": self.session_time_left,
            "session_duration": self.session_duration,
            "pit_speed_limit": self.pit_speed_limit,
            "game_paused": self.game_paused,
            "safety_car_status": self.safety_car_status
        }
