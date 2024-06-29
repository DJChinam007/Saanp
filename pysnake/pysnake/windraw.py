try:
    import pygame
    from pygame import gfxdraw
except ModuleNotFoundError:
    print("Module PyGame is not installed.")

import numpy as np
from pysnake.enum import Item

class WindowGame:
    """
    PySnake window, depends on pygame.
    
    Attributes
    ----------
    game : pysnake.game.Game
        Main game.
    pygame_win : pygame.display
        The pygame window.
    cell_size : int, optional
        Size of a pysnake's cell. The default is 50.
    bbox_game : tuple(int, int, int, int), optional
        Position and size of the game display. The default is (0, 0, 1000, 1000).
    color_palette: dict
        Colors used to draw all elements.
    """
    
    def __init__(self, game, pygame_win,
                 cell_size=50, 
                 bbox_game=(0, 0, 1000, 1000)):
        
        self.pygame_win = pygame_win
        self.game = game
        self.cell_size = cell_size
        self.bbox_game = bbox_game
        self.color_palette = {
            "background":     (255, 255, 255),
            "empty":          (37, 54, 69),
            "wall":           (32, 44, 55),
            "snake":          (46, 142, 212),
            "snake_head":     (46, 142, 212),
            "apple":          (227, 68, 52),
            "visible_snake":  (44, 112, 155),
            "visible_apple":  (237, 37, 27),
            "visible_wall":   (19, 28, 35),
            "vision":         (102, 119, 132),
            "vision_apple":   (237, 37, 27),
            "vision_snake":   (255, 0, 0)
        }

    def _draw_vision(self):
        """
        Draw the full vision sensor for all snakes in the game.
        """
        j0, i0, _, _ = self.bbox_game
        for snake in self.game.snakes:
            for vision in snake.full_vision:
                first_visible_item = vision.nearest_cells[0]
                i, j = first_visible_item.coord
                if first_visible_item.item is Item.APPLE:
                    color = self.color_palette['visible_apple']
                elif first_visible_item.item is Item.SNAKE:
                    color = self.color_palette['visible_snake']
                else:
                    color = self.color_palette['empty']
                pygame.draw.rect(self.pygame_win, color, 
                                 (j0 + j * self.cell_size, i0 + i * self.cell_size, 
                                  self.cell_size, self.cell_size)) 
                
                color = self.color_palette['vision']
                if first_visible_item.item is Item.APPLE:
                    color = self.color_palette['vision_apple']
                elif first_visible_item.item is Item.SNAKE:
                    color = self.color_palette['vision_snake']
                
                center = vision.center.coord
                end_point = vision.end_point
                start_point = (j0 + (center[1] + .5)*self.cell_size, 
                               i0 + (center[0] + .5)*self.cell_size)
                end_point = (j0 + (end_point[1] +.5)*self.cell_size,
                             i0 + (end_point[0] + .5)*self.cell_size)
                pygame.draw.line(self.pygame_win, color, start_point, end_point)

    def _draw_game(self, show_grid):
        """
        Draw the game's grid.

        Parameters
        ----------
        show_grid : bool
            Draw a grid.
        """
        game = self.game
        grid = game.grid
        height, width = grid.shape
        j0, i0, _, _ = self.bbox_game
        
        for i in range(height):
            for j in range(width):
                if grid[i, j].is_wall():
                    color = self.color_palette['wall']
                elif grid[i, j].is_empty():
                    color = self.color_palette['empty']
                    if show_grid and ((i +j)%2 == 1):
                        color = self.color_palette['wall']
                elif grid[i, j].is_snake():
                    color = self.color_palette['snake']
                elif grid[i, j].is_apple():
                    color = self.color_palette['apple']
                else:
                    continue
                
                pygame.draw.rect(self.pygame_win, color, 
                                 (j0 + j * self.cell_size, i0 + i * self.cell_size, 
                                  self.cell_size, self.cell_size))  
       
        for snake in self.game.snakes:
            i, j = snake.body[-1].coord
            color = self.color_palette['snake_head']
            pygame.draw.rect(self.pygame_win, color, 
                            (j0 + j * self.cell_size, i0 + i * self.cell_size, 
                             self.cell_size, self.cell_size))   
    
    def draw(self, show_grid=True, show_vision=False):
        """
        Draw and update the pygame window.

        Parameters
        ----------
        show_grid : bool, optional
            Show the grid if true. The default is True.
        show_vision : bool, optional
            Show the snakes vision if true. The default is False.
        """
        # height, width = pygame.display.get_surface().get_size()
        color = self.color_palette["background"]
        # pygame.draw.rect(self.pygame_win, color, (0, 0, width, height))  
        
        self._draw_game(show_grid)
        if show_vision:
            self._draw_vision()    
    
        pygame.display.update()