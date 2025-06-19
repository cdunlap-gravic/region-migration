import math
import os # NEW: Import os module for current working directory display

def display_header(header_type="default"):
    """Displays a formatted header based on the type."""
    if header_type == "welcome":
        print("\n" + "#" * 60)
        print("#" + " " * 58 + "#")
        print(f"#{'Minecraft WorldEdit Transfer Assistant':^58}#")
        print("#" + " " * 58 + "#")
        print("#" * 60)
        print("#" + " " * 58 + "#")
        print(f"#{'Welcome! This tool generates WorldEdit commands':^58}#")
        print(f"#{'to move structures between worlds.':^58}#")
        print("#" + " " * 58 + "#")
        print(f"#{'Please provide the requested information below.':^58}#")
        print("#" + " " * 58 + "#")
        print("#" * 60 + "\n")
    elif header_type == "review":
        print("\n" + "#" * 60)
        print(f"#{'REVIEW YOUR INPUTS':^58}#")
        print("#" * 60)
    elif header_type == "restart":
        print("\n" + "#" * 60)
        print(f"#{'Restarting Input Process':^58}#")
        print("#" * 60)
        print(f"#{'Let\'s try that again. Please re-enter the information.':^58}#")
        print(f"#{'Hit ENTER to keep the current value.':^58}#")
        print("#" * 60 + "\n")
    elif header_type == "generating":
        print("\n" + "-" * 60)
        print(f"{'Generating your WorldEdit commands...':^60}")
        print("-" * 60 + "\n")
    elif header_type == "complete":
        print("\n" + "#" * 80) # Increased width for final message
        print("#" * 80)
        print(f"{'#':<2}{'COMMAND GENERATION COMPLETE! YOUR ADVENTURE AWAITS!':^76}{'#':>2}")
        print("#" * 80)
        print("#" + " " * 78 + "#")
        print(f"#{'Your comprehensive list of Minecraft WorldEdit commands is ready.':^78}#")
        print(f"#{'':^78}#")
        print(f"#{'Copy them carefully and execute them in your Minecraft client, one by one.':^78}#")
        print(f"#{'Ensure each WorldEdit/server operation fully completes before proceeding.':^78}#")
        print(f"#{'':^78}#")
        print(f"#{'Transform your worlds, block by block!':^78}#")
        print(f"#{'':^78}#")
        print(f"#{'Let the building begin!':^78}#")
        print("#" + " " * 78 + "#")
        print("#" * 80)
        print("#" * 80 + "\n")

def get_input(prompt, default_value=None, value_type=str):
    """
    Prompts the user for input, showing a default value.
    Returns default_value (converted to value_type) if user hits Enter. Handles type conversion.
    """
    while True:
        try:
            display_prompt = prompt
            display_default_str = None
            if default_value is not None:
                # MODIFIED: Ensure default_value is correctly formatted for display if it's a tuple
                if value_type == tuple and isinstance(default_value, tuple):
                    display_default_str = ','.join(map(str, default_value))
                else:
                    display_default_str = str(default_value)
                display_prompt += f" [{display_default_str}]"
            
            user_input = input(display_prompt + ": ").strip()

            if user_input == "":
                if default_value is not None:
                    # FIX: Apply value_type conversion to default_value if empty input
                    if value_type == int:
                        return int(default_value) # Default value is already int if passed as int
                    elif value_type == tuple:
                        # Default value is a tuple, but might have been displayed as string
                        # Ensure it's returned as a tuple of ints
                        if isinstance(default_value, tuple):
                            return default_value
                        else: # If for some reason default_value came in as a string here
                            parts = [int(p.strip()) for p in str(default_value).split(',')]
                            if len(parts) != 3:
                                 raise ValueError(f"Invalid default tuple format during conversion: {default_value}")
                            return tuple(parts)
                    return default_value # For str type or other, return as is
                else:
                    print("Input cannot be empty. Please provide a value.")
                    continue
            
            # Original logic for non-empty input remains the same
            if value_type == int:
                return int(user_input)
            elif value_type == tuple:
                parts = [int(p.strip()) for p in user_input.split(',')]
                if len(parts) != 3:
                    raise ValueError("Coordinates must be X,Y,Z.")
                return tuple(parts)
            return user_input
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")

def get_yes_no_input(prompt, default_value=None):
    """
    Prompts for a yes/no input with validation and default handling.
    Returns True for 'yes', False for 'no'.
    """
    while True:
        display_prompt = prompt
        if default_value is not None:
            # Display 'Y' or 'n' based on default_value (True/False)
            default_char = 'Y' if default_value else 'n'
            display_prompt += f" ({default_char}/n) [{default_char}]"
        else:
            display_prompt += " (Y/n)" # Initial prompt, default is Yes if empty

        user_input = input(display_prompt + ": ").strip().lower() # Colon added for consistency

        if user_input == "":
            if default_value is not None:
                return default_value
            else: # First time prompt, default is Yes
                return True
        elif user_input in ['y', 'yes']:
            return True
        elif user_input in ['n', 'no']:
            return False
        else:
            print("Invalid response. Please enter 'y' or 'n'.")

def get_bounding_boxes(existing_boxes=None):
    """
    Gets a list of bounding boxes from the user.
    Allows 'KEEP' to retain existing list during re-prompts.
    """
    boxes = []
    if existing_boxes:
        print("\nCurrent Source Bounding Boxes:")
        for i, box in enumerate(existing_boxes):
            print(f"  {i+1}: ({box[0]},{box[1]},{box[2]}) to ({box[3]},{box[4]},{box[5]})")
    
    print("\nEnter Source Bounding Boxes (X1,Y1,Z1,X2,Y2,Z2 format).")
    print("Type 'DONE' when finished. Type 'KEEP' to retain current list.")

    idx = 1
    while True:
        prompt_text = f"Enter Source Bounding Box #{idx} (or 'DONE' or 'KEEP')"
        user_input = input(f"{prompt_text}: ").strip().upper()

        if user_input == 'DONE':
            break
        elif user_input == 'KEEP':
            if existing_boxes:
                return existing_boxes
            else:
                print("Cannot 'KEEP' as no existing boxes are present. Please enter boxes or 'DONE'.")
                continue
        
        try:
            coords = [int(p.strip()) for p in user_input.split(',')]
            if len(coords) != 6:
                raise ValueError("Bounding box must be X1,Y1,Z1,X2,Y2,Z2 (6 comma-separated numbers).")
            # Ensure X1 <= X2, Y1 <= Y2, Z1 <= Z2
            # This correctly handles negative coordinates as well
            coords = [min(coords[0], coords[3]), min(coords[1], coords[4]), min(coords[2], coords[5]),
                      max(coords[0], coords[3]), max(coords[1], coords[4]), max(coords[2], coords[5])]
            boxes.append(tuple(coords))
            idx += 1
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
    
    if not boxes and not existing_boxes: # If nothing entered and no existing boxes, force re-entry
        print("No bounding boxes entered. Please enter at least one bounding box.")
        return get_bounding_boxes(existing_boxes) 
    elif not boxes and existing_boxes: # If 'DONE' was hit on an empty new list but existing boxes were there, use existing.
        # This case handles hitting DONE without entering new boxes after seeing existing.
        # It's an implicit 'KEEP' if new list is empty and existing was shown.
        return existing_boxes
    return boxes

def calculate_sub_regions(bbox, sub_region_size, target_origin_start):
    """
    Calculates sub-regions for a given bounding box and target origin.
    Returns a list of (source_bbox, target_paste_coords) tuples.
    Handles negative coordinates correctly.
    """
    x1, y1, z1, x2, y2, z2 = bbox
    
    # Calculate dimensions
    dx = x2 - x1 + 1
    dy = y2 - y1 + 1 # Y-dimension is not split into sub-regions
    dz = z2 - z1 + 1

    sub_regions = []

    # Iterate through sub-regions
    # Use floor division for range steps to correctly cover all areas
    # For positive or negative, i_x and i_z are offsets from x1/z1
    for i_x in range(0, dx, sub_region_size):
        for i_z in range(0, dz, sub_region_size):
            # Source sub-region coordinates
            src_sub_x1 = x1 + i_x
            src_sub_y1 = y1
            src_sub_z1 = z1 + i_z
            
            src_sub_x2 = min(x1 + i_x + sub_region_size - 1, x2)
            src_sub_y2 = y2
            src_sub_z2 = min(z1 + i_z + sub_region_size - 1, z2)

            # Target paste coordinates (relative to original target origin)
            # target_origin_start is the base for the *first* sub-region.
            # Subsequent sub-regions paste at an offset relative to this origin.
            target_paste_x = target_origin_start[0] + i_x
            target_paste_y = target_origin_start[1] 
            target_paste_z = target_origin_start[2] + i_z
            
            sub_regions.append(
                ((src_sub_x1, src_sub_y1, src_sub_z1, src_sub_x2, src_sub_y2, src_sub_z2),
                 (target_paste_x, target_paste_y, target_paste_z))
            )
    return sub_regions

def main():
    # Store input values for re-prompting
    settings = {
        'source_world': None,
        'target_world': None,
        'creative_mode': None, # True/False
        'source_bounding_boxes': [],
        'target_paste_origin': None, # Stored as tuple of ints
        'sub_region_size': None, # Stored as int
        'save_to_file': None, # NEW: True/False flag for saving to file
        'output_filename': None # NEW: Stores the filename for output
    }
    
    # Store initial defaults for first run
    initial_creative_mode_default = True
    initial_save_to_file_default = True # NEW: Default to saving to file

    display_header(header_type="welcome")

    while True:
        # --- Get Inputs ---
        if settings['source_world'] is None: # First run
            settings['source_world'] = get_input("Source World Name")
            settings['target_world'] = get_input("Target World Name")
            settings['creative_mode'] = get_yes_no_input("Creative Mode needed?", default_value=initial_creative_mode_default)
            settings['source_bounding_boxes'] = get_bounding_boxes()
            settings['target_paste_origin'] = get_input("Target Paste Origin (X,Y,Z)", default_value=(0,0,0), value_type=tuple) 
            settings['sub_region_size'] = get_input("Sub-Region Size", default_value=64, value_type=int)
            # NEW: Prompts for file output settings
            settings['save_to_file'] = get_yes_no_input("Save commands to a file?", default_value=initial_save_to_file_default)
            if settings['save_to_file']:
                settings['output_filename'] = get_input("Enter filename (e.g., commands.txt)", default_value="commands.txt")
        else: # Re-prompt after 'n' confirmation
            display_header(header_type="restart")
            settings['source_world'] = get_input("Source World Name", default_value=settings['source_world'])
            settings['target_world'] = get_input("Target World Name", default_value=settings['target_world'])
            settings['creative_mode'] = get_yes_no_input("Creative Mode needed?", default_value=settings['creative_mode'])
            settings['source_bounding_boxes'] = get_bounding_boxes(existing_boxes=settings['source_bounding_boxes'])
            # Pass the actual tuple as default_value here; get_input will format it for display
            settings['target_paste_origin'] = get_input("Target Paste Origin (X,Y,Z)", default_value=settings['target_paste_origin'], value_type=tuple)
            settings['sub_region_size'] = get_input("Sub-Region Size", default_value=settings['sub_region_size'], value_type=int)
            # NEW: Re-prompts for file output settings
            settings['save_to_file'] = get_yes_no_input("Save commands to a file?", default_value=settings['save_to_file'])
            if settings['save_to_file']:
                # Ensure output_filename has a default if it was None before (e.g., if user changed from No to Yes)
                filename_default = settings['output_filename'] if settings['output_filename'] else "commands.txt"
                settings['output_filename'] = get_input("Enter filename (e.g., commands.txt)", default_value=filename_default)
            else:
                settings['output_filename'] = None # Clear filename if user opts out of saving

        # Calculate total sub-regions for confirmation
        all_sub_regions = []
        for bbox in settings['source_bounding_boxes']:
            all_sub_regions.extend(calculate_sub_regions(bbox, settings['sub_region_size'], settings['target_paste_origin']))
        
        total_sub_regions = len(all_sub_regions)

        # --- Review and Confirm ---
        display_header(header_type="review")
        print(f"Source World: {settings['source_world']}")
        print(f"Target World: {settings['target_world']}")
        print(f"Set Gamemode to Creative: {'Yes' if settings['creative_mode'] else 'No'}")
        print("Source Bounding Boxes:")
        for i, box in enumerate(settings['source_bounding_boxes']):
            print(f"  Box {i+1}: ({box[0]}, {box[1]}, {box[2]}) to ({box[3]}, {box[4]}, {box[5]})")
        # Ensure target_paste_origin is displayed as X,Y,Z even if it was corrected
        print(f"Target Paste Origin: ({settings['target_paste_origin'][0]}, {settings['target_paste_origin'][1]}, {settings['target_paste_origin'][2]})")
        print(f"Sub-Region Size: {settings['sub_region_size']}")
        print(f"Total Sub-Regions to Generate: {total_sub_regions}")
        print("#" * 60)
        print(f"#{'CAUTION: Large operations will be generated!':^58}#")
        print(f"#{'THIS IS YOUR LAST CHANCE TO REVIEW AND CONFIRM!':^58}#")
        # NEW: Add file output info to review
        if settings['save_to_file']:
            print(f"Output to File: Yes (Filename: {settings['output_filename']})")
        else:
            print("Output to File: No (Commands will only be printed to console)")
        
        print("#" * 60)

        confirm = get_yes_no_input("Proceed with command generation?")
        
        if confirm:
            break # Exit the input loop and proceed to generation
        else:
            print("\nOkay, let's re-enter the details.")
            # Loop continues, prompting again with existing values

    # --- Generate Commands ---
    display_header(header_type="generating")

    output_file_handle = None # NEW: Initialize file handle
    if settings['save_to_file']: # NEW: Check if saving to file is enabled
        try:
            # NEW: Open file using 'with' for automatic closing
            output_file_handle = open(settings['output_filename'], 'w')
            print(f"Commands will also be saved to '{settings['output_filename']}' in the current directory ({os.getcwd()})\n")
        except IOError as e: # NEW: Error handling for file operations
            print(f"ERROR: Could not open file '{settings['output_filename']}' for writing: {e}")
            print("Commands will only be printed to console.")
            settings['save_to_file'] = False # Disable file saving if error occurs
            if output_file_handle: # Safety check, though 'with' should handle it
                output_file_handle.close()

    # NEW: Define a helper function to print to console AND write to file
    def print_and_write(text):
        print(text)
        if settings['save_to_file'] and output_file_handle: # Check if file saving is enabled AND file is open
            output_file_handle.write(text + '\n')
    sub_region_counter = 0
    for bbox_idx, bbox in enumerate(settings['source_bounding_boxes']):
        current_bbox_sub_regions = calculate_sub_regions(bbox, settings['sub_region_size'], settings['target_paste_origin'])
        
        for i, (src_coords, target_coords) in enumerate(current_bbox_sub_regions):
            sub_region_counter += 1
            # MODIFIED: All print() calls replaced with print_and_write()
            print_and_write(f"# --- SUB-REGION {sub_region_counter} of {total_sub_regions} (Source: {src_coords[0]},{src_coords[1]},{src_coords[2]} to {src_coords[3]},{src_coords[4]},{src_coords[5]} -> Target: {target_coords[0]},{target_coords[1]},{target_coords[2]}) ---")
            print_and_write(f"/mvtp {settings['source_world']}") 
            print_and_write(f"/tp {src_coords[0]} {src_coords[1]} {src_coords[2]}")
            if settings['creative_mode']:
                print_and_write("/gamemode creative")
            print_and_write(f"//sel {src_coords[0]},{src_coords[1]},{src_coords[2]} {src_coords[3]},{src_coords[4]},{src_coords[5]}")
            print_and_write(f"//copy -be")
            print_and_write(f"/mvtp {settings['target_world']}")
            print_and_write(f"/tp {target_coords[0]} {target_coords[1]} {target_coords[2]}")
            if settings['creative_mode']:
                print_and_write("/gamemode creative")
            print_and_write(f"//paste -be\n") # Kept one newline for spacing between regions

    # NEW: Final message about file saving, after all commands are written
    if settings['save_to_file'] and output_file_handle:
        print(f"\nAll commands successfully saved to '{settings['output_filename']}'.")
    
    display_header(header_type="complete")

if __name__ == "__main__":
    main()