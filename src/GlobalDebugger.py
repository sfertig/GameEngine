def GlobalDebugger(log_queue):
    """
    Runs in an isolated process. Must completely rebuild its 
    own window drivers and pump events immediately to become visible.
    """
    import pygame # Import inside the process to ensure clean namespace isolation
    
    # RULE 1: Fresh initialization of the sub-process multimedia context
    pygame.init()
    
    # RULE 3: Use traditional display modes for sub-processes to ensure OS hook compatibility
    # Set window size (e.g., 400x600)
    screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("Engine Debug Log")
    
    font = pygame.font.Font(None, 22)
    clock = pygame.time.Clock()
    displayed_logs = ["--- Debugger Online ---"]
    
    running = True
    while running:
        # RULE 2: Pump events immediately so Windows displays the window framework
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Drain the communication tube 
        while not log_queue.empty():
            try:
                msg = log_queue.get(block=False)
                displayed_logs.append(msg)
                if len(displayed_logs) > 25:
                    displayed_logs.pop(1)
            except:
                break
                
        # Draw the logs onto the screen
        screen.fill((15, 15, 15))
        
        y = 15
        for log in displayed_logs:
            color = (255, 80, 80) if "Error" in log else (220, 220, 220)
            txt = font.render(log, True, color)
            screen.blit(txt, (15, y))
            y += 22
            
        # Push the frame buffer onto the screen monitor
        pygame.display.flip()
        
        # Keep frame times light to optimize host CPU execution
        clock.tick(30)
        
    pygame.quit()