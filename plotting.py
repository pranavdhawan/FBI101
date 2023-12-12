import pygame
from datetime import datetime

def parse_logs(log_file_path):
    coordinates = []

    with open(log_file_path, 'r') as file:
        for line in file:
            parts = line.split('_')
            timestamp_str, rest = parts[0], '-'.join(parts[1:])
            try:
                timestamp = datetime.strptime(timestamp_str.strip(), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue

            common_coordinates_str = rest.split(':')[-1].strip()
            if common_coordinates_str.startswith('(') and common_coordinates_str.endswith(')'):
                common_coordinates_str = common_coordinates_str[1:-1]
                common_coordinates = list(map(int, common_coordinates_str.split(',')))
                if len(common_coordinates) == 2:
                    app_name = rest.split(':')[1].strip()
                    coordinates.append((timestamp, common_coordinates[0], common_coordinates[1], app_name))

    return coordinates



def draw_dots(coordinates):
    pygame.init()

    screen_width, screen_height = 1680, 1050
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill((255, 255, 255))

    dot_radius = 5

    font_path = pygame.font.get_default_font() 
    font = pygame.font.Font(font_path, 7)
    
    for coord in coordinates:
        timestamp, common_eye_x, common_eye_y, app_name = coord

        dot_color = (255, 0, 0) 
        dot_position = (common_eye_x, common_eye_y)
        pygame.draw.circle(screen, dot_color, dot_position, dot_radius)

        text = font.render(f"{timestamp}", True, (0, 0, 0))

        text_rect = text.get_rect(center=(common_eye_x + 10, common_eye_y))
        screen.blit(text, text_rect)

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    log_file_path = "console.txt"  
    coordinates = parse_logs(log_file_path)
    draw_dots(coordinates)
