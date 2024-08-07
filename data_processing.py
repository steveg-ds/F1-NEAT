import socket
from data_classes import *
import time

class DataProcessor:
    def collect_packet(self):
        def listen_udp(ip, port):
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.bind((ip, port))

            encountered_packet_ids = set()
            stored_data = {}

            try:
                while len(encountered_packet_ids) < 4:  # Changed to avoid hardcoded value
                    data, address = udp_socket.recvfrom(2000)
                    packet_header = PacketHeader(data)
                    packet_header_dict = packet_header.to_dict()
                    packet_id = packet_header_dict['packet_id']

                    if packet_id in [0, 2, 6, 7] and packet_id not in encountered_packet_ids:
                        encountered_packet_ids.add(packet_id)

                        if packet_id == 0:
                            stored_data['car_motion'] = CarMotionData(data[29:]).to_dict()
                        elif packet_id == 2:
                            stored_data['lap_data'] = LapData(data[29:]).to_dict()
                        elif packet_id == 6:
                            stored_data['telemetry_data'] = CarTelemetryData(data[29:]).to_dict()
                        elif packet_id == 7:
                            stored_data['car_status'] = CarStatusData(data[29:]).to_dict()

                yield stored_data

            except Exception as e:
                print(f"Error occurred while collecting packet data: {e}")
            finally:
                udp_socket.close()

        try:
            for data in listen_udp("127.0.0.1", 20777):
                cols = {
                    "lap_data": ['last_lap_time_ms', 'current_lap_time_ms', 'lap_distance',
                                 'current_lap_invalid'],
                    "car_motion": ['world_position_x', 'world_position_y', 'world_position_z', 'world_velocity_x',
                                   'world_velocity_y', 'world_velocity_z', 'world_forward_dir_x', 'world_forward_dir_y',
                                   'world_forward_dir_z', 'world_right_dir_x', 'world_right_dir_y', 'world_right_dir_z',
                                   'g_force_lateral', 'g_force_longitudinal', 'g_force_vertical', 'yaw', 'pitch',
                                   'roll'],
                    "telemetry_data": ['speed', 'throttle', 'steer', 'brake', 'drs', 'surface_type',
                                       'clutch', 'gear'],
                }

                filtered_data = {}
                for packet_type, keys in cols.items():
                    packet_data = data.get(packet_type, {})
                    filtered_values = {key: packet_data.get(key, None) for key in keys}

                    if filtered_values:
                        filtered_data.update(filtered_values)

                # Summing surface_type values
                filtered_data['surface_type'] = sum(filtered_data.get('surface_type', []))
                # time.sleep(0.33)
                yield filtered_data

        except Exception as e:
            print("Data Collection Problem:", e)

# data_processor = DataProcessor()
# while True:
#     print(next(data_processor.collect_packet()))
