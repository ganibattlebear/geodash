"""
Platformer Game
"""
import pyglet
import playsound
import arcade
import os
import time
# Constants (alter for your game or delete)
SCREEN_WIDTH = 2048
SCREEN_HEIGHT = 1536
SCREEN_TITLE = "Geometry Dash bootleg"
CHARACTER_SCALING = 1
TILE_SCALING = 1
COIN_SCALING = 1
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)
PLAYER_MOVEMENT_SPEED = 17
GRAVITY = 2
PLAYER_JUMP_SPEED = 24
PLAYER_START_X = 64
PLAYER_START_Y = 961

GAME_RUNNING = 2
GAME_OVER = 3
# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 128
RIGHT_VIEWPORT_MARGIN = 1700
BOTTOM_VIEWPORT_MARGIN = 950
TOP_VIEWPORT_MARGIN = 300

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        self.wall_list = None
        self.player_list = None
        self.spike_or_bad_list = None
        self.player_sprite = None
        self.allsprites = None
        self.physics_engine = None
        self.view_bottom = 0
        self.view_left = 0
        self.danube = arcade.load_sound("1geosong.wav")
        self.end_of_map = 0
        self.current_state = GAME_RUNNING
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup_lvl_1(self):
        """ Set up the game here. Call this function to restart the game. """
        self.view_bottom = 0
        self.view_left = 0
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.spike_or_bad_list = arcade.SpriteList()
        self.allsprites = arcade.SpriteList()
        self.spike = arcade.Sprite("spike1.png")
        self.spike_or_bad_list.append(self.spike)
        self.allsprites.append(self.spike)
        """"""
        arcade.play_sound(self.danube)
        """"""
 # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = arcade.Sprite("geodash-player.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 961
        self.player_list.append(self.player_sprite)
        self.allsprites.append(self.player_sprite)
        # --- Load in a map from the tiled editor ---
        platforms_layer_name = 'Platforms'
        bad_layer_name = 'Spikes'
        # Name of map file to load
        map_name = f"GeoDash.tmx"
        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)
        # Calculate the right edge of the my_map in pixels
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE
        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)

        # -- Coins
        #self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name, TILE_SCALING)
        
        # -- Spikes or Bad Layer
        self.spike_or_bad_list = arcade.tilemap.process_layer(my_map, bad_layer_name, TILE_SCALING)
        

        #create physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)


        pass
    def on_draw(self):
        """ Render the screen. """
        #Clear screen to BG
        arcade.start_render()
        self.wall_list.draw()
        self.player_list.draw()
        self.spike_or_bad_list.draw()
        self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        
    def on_key_press(self, key, modifiers):
        #Called whenever a key is pressed. I N P U T S
        if key == arcade.key.UP or key == arcade.key.W and self.current_state == GAME_RUNNING:
             if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                #arcade.play_sound(self.jump_sound)
        #if key == arcade.key.S:
            #import sys
            #subprocess.call(sys.executable + ' "' + os.path.realpath(__file__) + '"')
            #main()
            

    #def on_key_release(self, key, modifiers):
        
        
    def update(self, delta_time):
        """Movement and Game Logic"""
        if self.current_state == GAME_RUNNING:
            
            #Calls update on all sprites
            
            self.physics_engine.update()
            self.player_list.update()
            # --- Manage Scrolling ---

            # Track if we need to change the viewport

            changed = False
            
            # Did the player fall off the map?
            
            if self.player_sprite.center_y < -500:
                """"""
                #arcade.stop_sound
                """"""
                #arcade.play_sound("1geosong.wav")
                """"""
                self.player_sprite.center_x = PLAYER_START_X
                self.player_sprite.center_y = PLAYER_START_Y
                
                # Set the camera to the start
                
                self.view_left = 0
                self.view_bottom = 0
                changed = True
            if self.player_sprite.center_x >= self.end_of_map - 3072:
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                arcade.close_window()
                self.current_state = GAME_OVER
            # Did the player touch something they should not?
            
            if arcade.check_for_collision_with_list(self.player_sprite, self.spike_or_bad_list):
                #PUT EXPLOSION HERE
            
                """"""
                #arcade.stop_sound
                """"""
                #arcade.play_sound("1geosong.wav")
                """"""
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                self.player_sprite.center_x = PLAYER_START_X
                self.player_sprite.center_y = PLAYER_START_Y
            
                # Set the camera to the start
                
                self.view_left = 0
                self.view_bottom = 0
                changed = True
            
        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)
def main():
    """ Main method """
    window = MyGame()
    window.setup_lvl_1()
    arcade.run()



# if __name__ == "__main__":
     #main()
main()
