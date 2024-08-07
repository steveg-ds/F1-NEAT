import struct

class PacketHeader:
    """
    This class represents the header of a data packet. It parses raw binary data to extract various fields.

    Attributes:
        packet_format (int): The packet format version.
        game_year (int): The year of the game.
        game_major_version (int): The major version of the game.
        game_minor_version (int): The minor version of the game.
        packet_version (int): The version of the packet.
        packet_id (int): The ID of the packet.
        session_uid (int): The unique session identifier.
        session_time (float): The session time.
        frame_identifier (int): The frame identifier.
        overall_frame_identifier (int): The overall frame identifier.
        player_car_index (int): The index of the player's car.
        secondary_player_car_index (int): The index of the secondary player's car.
    """

    def __init__(self, data):
        self.data = data

    def to_dict(self):
        """
        Converts the PacketHeader instance to a dictionary.

        Returns:
            dict: A dictionary containing all the attributes of the instance.
        """
        return {
            "packet_format": int.from_bytes(self.data[0:2], byteorder='little'),
            "game_year": int.from_bytes(self.data[2:3], byteorder='little'),
            "game_major_version": int.from_bytes(self.data[3:4], byteorder='little'),
            "game_minor_version": int.from_bytes(self.data[4:5], byteorder='little'),
            "packet_version": int.from_bytes(self.data[5:6], byteorder='little'),
            "packet_id": int.from_bytes(self.data[6:7], byteorder='little'),
            "session_uid": int.from_bytes(self.data[7:15], byteorder='little'),
            "session_time": struct.unpack('<f', self.data[15:19])[0],
            "frame_identifier": int.from_bytes(self.data[19:23], byteorder='little'),
            "overall_frame_identifier": int.from_bytes(self.data[23:27], byteorder='little'),
            "player_car_index": int.from_bytes(self.data[27:28], byteorder='little'),
            "secondary_player_car_index": int.from_bytes(self.data[28:29], byteorder='little')
        }


class CarMotionData:
    """
    This class represents the motion data of a car. It parses raw binary data to extract various motion parameters.

    Attributes:
        world_position_x (float): The x-coordinate of the world position.
        world_position_y (float): The y-coordinate of the world position.
        world_position_z (float): The z-coordinate of the world position.
        world_velocity_x (float): The x-component of the world velocity.
        world_velocity_y (float): The y-component of the world velocity.
        world_velocity_z (float): The z-component of the world velocity.
        world_forward_dir_x (int): The x-component of the world forward direction.
        world_forward_dir_y (int): The y-component of the world forward direction.
        world_forward_dir_z (int): The z-component of the world forward direction.
        world_right_dir_x (int): The x-component of the world right direction.
        world_right_dir_y (int): The y-component of the world right direction.
        world_right_dir_z (int): The z-component of the world right direction.
        g_force_lateral (float): The lateral g-force.
        g_force_longitudinal (float): The longitudinal g-force.
        g_force_vertical (float): The vertical g-force.
        yaw (float): The yaw angle.
        pitch (float): The pitch angle.
        roll (float): The roll angle.
    """

    def __init__(self, data):
        self.data = data

    def to_dict(self):
        """
        Converts the CarMotionData instance to a dictionary.

        Returns:
            dict: A dictionary containing all the attributes of the instance.
        """
        return {
            "world_position_x": struct.unpack('<f', self.data[0:4])[0],
            "world_position_y": struct.unpack('<f', self.data[4:8])[0],
            "world_position_z": struct.unpack('<f', self.data[8:12])[0],
            "world_velocity_x": struct.unpack('<f', self.data[12:16])[0],
            "world_velocity_y": struct.unpack('<f', self.data[16:20])[0],
            "world_velocity_z": struct.unpack('<f', self.data[20:24])[0],
            "world_forward_dir_x": struct.unpack('<h', self.data[24:26])[0],
            "world_forward_dir_y": struct.unpack('<h', self.data[26:28])[0],
            "world_forward_dir_z": struct.unpack('<h', self.data[28:30])[0],
            "world_right_dir_x": struct.unpack('<h', self.data[30:32])[0],
            "world_right_dir_y": struct.unpack('<h', self.data[32:34])[0],
            "world_right_dir_z": struct.unpack('<h', self.data[34:36])[0],
            "g_force_lateral": struct.unpack('<f', self.data[36:40])[0],
            "g_force_longitudinal": struct.unpack('<f', self.data[40:44])[0],
            "g_force_vertical": struct.unpack('<f', self.data[44:48])[0],
            "yaw": struct.unpack('<f', self.data[48:52])[0],
            "pitch": struct.unpack('<f', self.data[52:56])[0],
            "roll": struct.unpack('<f', self.data[56:60])[0]
        }


class LapData:
    """
    This class represents the lap data of a car. It parses raw binary data to extract various lap-related parameters.

    Attributes:
        last_lap_time_ms (int): The time of the last lap in milliseconds.
        current_lap_time_ms (int): The time of the current lap in milliseconds.
        sector1_time_ms (int): The time of the first sector in milliseconds.
        sector1_time_minutes (int): The minutes part of the first sector time.
        sector2_time_ms (int): The time of the second sector in milliseconds.
        sector2_time_minutes (int): The minutes part of the second sector time.
        delta_to_car_in_front_ms (int): The delta time to the car in front in milliseconds.
        delta_to_race_leader_ms (int): The delta time to the race leader in milliseconds.
        lap_distance (float): The distance covered in the current lap.
        total_distance (float): The total distance covered in the race.
        safety_car_delta (float): The delta time to the safety car.
        car_position (int): The position of the car in the race.
        current_lap_num (int): The current lap number.
        pit_status (int): The pit status of the car.
        num_pit_stops (int): The number of pit stops made.
        sector (int): The current sector.
        current_lap_invalid (int): Whether the current lap is invalid.
        penalties (int): The number of penalties received.
        total_warnings (int): The total number of warnings received.
        corner_cutting_warnings (int): The number of corner-cutting warnings received.
        num_unserved_drive_through_pens (int): The number of unserved drive-through penalties.
        num_unserved_stop_go_pens (int): The number of unserved stop-go penalties.
        grid_position (int): The grid position of the car.
        driver_status (int): The status of the driver.
        result_status (int): The result status of the car.
        pit_lane_timer_active (int): Whether the pit lane timer is active.
        pit_lane_time_in_lane_ms (int): The time spent in the pit lane in milliseconds.
        pit_stop_timer_in_ms (int): The time of the pit stop in milliseconds.
        pit_stop_should_serve_pen (int): Whether the pit stop should serve a penalty.
    """

    def __init__(self, data):
       self.data = data
       
    def to_dict(self):
        """
        Converts the LapData instance to a dictionary.

        Returns:
            dict: A dictionary containing all the attributes of the instance.
        """
        return {
            "last_lap_time_ms": int.from_bytes(self.data[0:4], byteorder='little'),
            "current_lap_time_ms": int.from_bytes(self.data[4:8], byteorder='little'),
            "sector1_time_ms": int.from_bytes(self.data[8:10], byteorder='little'),
            "sector1_time_minutes": int.from_bytes(self.data[10:11], byteorder='little'),
            "sector2_time_ms": int.from_bytes(self.data[11:13], byteorder='little'),
            "sector2_time_minutes": int.from_bytes(self.data[13:14], byteorder='little'),
            "delta_to_car_in_front_ms": int.from_bytes(self.data[14:16], byteorder='little'),
            "delta_to_race_leader_ms": int.from_bytes(self.data[16:18], byteorder='little'),
            "lap_distance": struct.unpack('<f', self.data[18:22])[0],
            "total_distance": struct.unpack('<f', self.data[22:26])[0],
            "safety_car_delta": struct.unpack('<f', self.data[26:30])[0],
            "car_position": int.from_bytes(self.data[30:31], byteorder='little'),
            "current_lap_num": int.from_bytes(self.data[31:32], byteorder='little'),
            "pit_status": int.from_bytes(self.data[32:33], byteorder='little'),
            "num_pit_stops": int.from_bytes(self.data[33:34], byteorder='little'),
            "sector": int.from_bytes(self.data[34:35], byteorder='little'),
            "current_lap_invalid": int.from_bytes(self.data[35:36], byteorder='little'),
            "penalties": int.from_bytes(self.data[36:37], byteorder='little'),
            "total_warnings": int.from_bytes(self.data[37:38], byteorder='little'),
            "corner_cutting_warnings": int.from_bytes(self.data[38:39], byteorder='little'),
            "num_unserved_drive_through_pens": int.from_bytes(self.data[39:40], byteorder='little'),
            "num_unserved_stop_go_pens": int.from_bytes(self.data[40:41], byteorder='little'),
            "grid_position": int.from_bytes(self.data[41:42], byteorder='little'),
            "driver_status": int.from_bytes(self.data[42:43], byteorder='little'),
            "result_status": int.from_bytes(self.data[43:44], byteorder='little'),
            "pit_lane_timer_active": int.from_bytes(self.data[44:45], byteorder='little'),
            "pit_lane_time_in_lane_ms": int.from_bytes(self.data[45:47], byteorder='little'),
            "pit_stop_timer_in_ms": int.from_bytes(self.data[47:49], byteorder='little'),
            "pit_stop_should_serve_pen": int.from_bytes(self.data[49:50], byteorder='little')
        }

class CarData:
    """
    This class represents a packet containing motion data for multiple cars. It parses raw binary data to extract the header and car motion data.

    Attributes:
        header (PacketHeader): The header of the packet.
        car_motion_data (list): A list of CarMotionData objects for each car.
    """

    def __init__(self, data):
        self.header = PacketHeader(data[0:29])
        self.car_motion_data = []
        offset = 29
        car_data_size = 60  # Each CarMotionData object occupies 60 bytes
        num_cars = 22

        for i in range(num_cars):
            car_data = data[offset + i * car_data_size: offset + (i + 1) * car_data_size]
            self.car_motion_data.append(CarMotionData(car_data))

    def to_dict(self):
        """
        Converts the PacketCarMotionData instance to a dictionary.

        Returns:
            dict: A dictionary containing the header and car motion data.
        """
        return {
            "header": self.header.to_dict(),
            "car_motion_data": [car_data.to_dict() for car_data in self.car_motion_data]
        }

class CarTelemetryData:
    """
    This class represents telemetry data for a car, parsed from raw binary data.

    Attributes:
        speed (int): The speed of the car.
        throttle (float): The throttle input value.
        steer (float): The steering input value.
        brake (float): The brake input value.
        clutch (int): The clutch input value.
        gear (int): The current gear of the car.
        engine_rpm (int): The engine RPM.
        drs (int): The DRS (Drag Reduction System) status.
        rev_lights_percent (int): The percentage of the RPM rev lights active.
        rev_lights_bit_value (int): The bit value of the RPM rev lights.
        brakes_temperature (list of int): The temperature of the brakes.
        tyres_surface_temperature (list of int): The surface temperature of the tyres.
        tyres_inner_temperature (list of int): The inner temperature of the tyres.
        engine_temperature (int): The temperature of the engine.
        tyres_pressure (list of float): The pressure of the tyres.
        surface_type (list of int): The type of surface the tyres are currently on.
    """

    def __init__(self, data):
        """
        Initializes the CarTelemetryData instance from raw binary data.

        Args:
            data (bytes): The raw binary data from which the telemetry data is parsed.
        """
        self.data = data

    def to_dict(self):
        """
        Converts the CarTelemetryData instance to a dictionary.

        Returns:
            dict: A dictionary containing all the attributes of the instance.
        """
        return {
            "speed": int.from_bytes(self.data[0:2], byteorder='little'),
            "throttle": struct.unpack('<f', self.data[2:6])[0],
            "steer": struct.unpack('<f', self.data[6:10])[0],
            "brake": struct.unpack('<f', self.data[10:14])[0],
            "clutch": int.from_bytes(self.data[14:15], byteorder='little'),
            "gear": int.from_bytes(self.data[15:16], byteorder='little'),
            "engine_rpm": int.from_bytes(self.data[16:18], byteorder='little'),
            "drs": int.from_bytes(self.data[18:19], byteorder='little'),
            "rev_lights_percent": int.from_bytes(self.data[19:20], byteorder='little'),
            "rev_lights_bit_value": int.from_bytes(self.data[20:22], byteorder='little'),
            "brakes_temperature": [int.from_bytes(self.data[i:i + 2], byteorder='little') for i in range(22, 30, 2)],
            "tyres_surface_temperature": [int.from_bytes(self.data[i:i + 1], byteorder='little') for i in range(30, 34)],
            "tyres_inner_temperature": [int.from_bytes(self.data[i:i + 1], byteorder='little') for i in range(34, 38)],
            "engine_temperature": int.from_bytes(self.data[38:40], byteorder='little'),
            "tyres_pressure": [struct.unpack('<f', self.data[i:i + 4])[0] for i in range(40, 56, 4)],
            "surface_type": [int.from_bytes(self.data[i:i + 1], byteorder='little') for i in range(56, 60)]
        }
    
class CarStatusData:
    """
    This class represents the status data of a car, parsed from raw binary data.

    Attributes:
        traction_control (int): The traction control setting.
        anti_lock_brakes (int): The anti-lock brakes status.
        fuel_mix (int): The fuel mixture setting.
        front_brake_bias (int): The front brake bias.
        pit_limiter_status (int): The pit limiter status.
        fuel_in_tank (float): The amount of fuel currently in the tank.
        fuel_capacity (float): The total fuel capacity.
        fuel_remaining_laps (float): The number of laps the remaining fuel will last.
        max_rpm (int): The maximum RPM of the engine.
        idle_rpm (int): The idle RPM of the engine.
        max_gears (int): The maximum number of gears.
        drs_allowed (int): The status of the DRS (Drag Reduction System) allowance.
        drs_activation_distance (int): The distance required to activate DRS.
        actual_tyre_compound (int): The actual compound of the tyres.
        visual_tyre_compound (int): The visual representation of the tyre compound.
        tyres_age_laps (int): The number of laps the tyres have been used.
        vehicle_fia_flags (int): The FIA flags associated with the vehicle.
        engine_power_ice (float): The power of the internal combustion engine (ICE).
        engine_power_mguk (float): The power of the MGUK (Motor Generator Unit - K).
        ers_store_energy (float): The amount of energy stored in the ERS (Energy Recovery System).
        ers_deploy_mode (int): The deployment mode of the ERS.
        ers_harvested_this_lap_mguk (float): The energy harvested by the MGUK this lap.
        ers_harvested_this_lap_mguh (float): The energy harvested by the MGuh this lap.
        ers_deployed_this_lap (float): The energy deployed by the ERS this lap.
        network_paused (int): The network paused status.
    """

    def __init__(self, data):
        """
        Initializes the CarStatusData instance from raw binary data.

        Args:
            data (bytes): The raw binary data from which the car status data is parsed.
        """
        self.data = data

    def to_dict(self):
        """
        Converts the CarStatusData instance to a dictionary.

        Returns:
            dict: A dictionary containing all the attributes of the instance.
        """
        return {
            "traction_control": int.from_bytes(self.data[0:1], byteorder='little'),
            "anti_lock_brakes": int.from_bytes(self.data[1:2], byteorder='little'),
            "fuel_mix": int.from_bytes(self.data[2:3], byteorder='little'),
            "front_brake_bias": int.from_bytes(self.data[3:4], byteorder='little'),
            "pit_limiter_status": int.from_bytes(self.data[4:5], byteorder='little'),
            "fuel_in_tank": struct.unpack('<f', self.data[5:9])[0],
            "fuel_capacity": struct.unpack('<f', self.data[9:13])[0],
            "fuel_remaining_laps": struct.unpack('<f', self.data[13:17])[0],
            "max_rpm": int.from_bytes(self.data[17:19], byteorder='little'),
            "idle_rpm": int.from_bytes(self.data[19:21], byteorder='little'),
            "max_gears": int.from_bytes(self.data[21:22], byteorder='little'),
            "drs_allowed": int.from_bytes(self.data[22:23], byteorder='little'),
            "drs_activation_distance": int.from_bytes(self.data[23:25], byteorder='little'),
            "actual_tyre_compound": int.from_bytes(self.data[25:26], byteorder='little'),
            "visual_tyre_compound": int.from_bytes(self.data[26:27], byteorder='little'),
            "tyres_age_laps": int.from_bytes(self.data[27:28], byteorder='little'),
            "vehicle_fia_flags": int.from_bytes(self.data[28:29], byteorder='little'),
            "engine_power_ice": struct.unpack('<f', self.data[29:33])[0],
            "engine_power_mguk": struct.unpack('<f', self.data[33:37])[0],
            "ers_store_energy": struct.unpack('<f', self.data[37:41])[0],
            "ers_deploy_mode": int.from_bytes(self.data[41:42], byteorder='little'),
            "ers_harvested_this_lap_mguk": struct.unpack('<f', self.data[42:46])[0],
            "ers_harvested_this_lap_mguh": struct.unpack('<f', self.data[46:50])[0],
            "ers_deployed_this_lap": struct.unpack('<f', self.data[50:54])[0],
            "network_paused": int.from_bytes(self.data[54:55], byteorder='little')
        }
        
class PacketLapData:
    """
    This class represents a packet containing lap data for multiple cars. It parses raw binary data to extract the header and lap data.

    Attributes:
        header (PacketHeader): The header of the packet.
        lap_data (list): A list of LapData objects for each car.
    """

    def __init__(self, data):
        self.header = PacketHeader(data[0:29])
        self.lap_data = []
        offset = 29
        car_data_size = 50  # Each LapData object occupies 50 bytes
        num_cars = 22

        for i in range(num_cars):
            car_data = data[offset + i * car_data_size: offset + (i + 1) * car_data_size]
            self.lap_data.append(LapData(car_data))

    def to_dict(self):
        """
        Converts the PacketLapData instance to a dictionary.

        Returns:
            dict: A dictionary containing the header and lap data.
        """
        return {
            "header": self.header.to_dict(),
            "lap_data": [lap_data.to_dict() for lap_data in self.lap_data]
        }

# Define the parsing functions for each packet type
def parse_packet_car_motion_data(data):
    """
    Parses the given raw binary data as a PacketCarMotionData instance.

    Args:
        data (bytes): The raw binary data of the packet.

    Returns:
        PacketCarMotionData: The parsed PacketCarMotionData instance.
    """
    return PacketCarMotionData(data).to_dict()

def parse_packet_lap_data(data):
    """
    Parses the given raw binary data as a PacketLapData instance.

    Args:
        data (bytes): The raw binary data of the packet.

    Returns:
        PacketLapData: The parsed PacketLapData instance.
    """
    return PacketLapData(data).to_dict()

