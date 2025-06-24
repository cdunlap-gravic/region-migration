#############################
## 
## TODO:
##  - migrate to main.py
##  - clean up what I can,
##  - config system, for repeated jobs, save profiles etc.
##  - 
## 
#############################

import math
import os
import json

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
        print("#" + " " * 58 + "#")
        print("#" * 60 + "\n")
    elif header_type == "generating":
        print("\n" + "-" * 60)
        print(f"{'Generating your WorldEdit commands...':^60}")
        print("-" * 60 + "\n")
    elif header_type == "complete":
        print("\n" + "#" * 80)
        print("#" * 80)
        print(f"{'#':<2}{'COMMAND GENERATION COMPLETE! YOUR ADVENTURE AWAITS!':^76}{'#':>2}")
        print("#" * 80)
        print("#" + " " * 78 + "#")
        print(f"#{'Your comprehensive list of Minecraft WorldEdit commands is ready.':^76}#")
        print(f"#{'':^76}#")
        print(f"#{'Copy them carefully and execute them in your Minecraft client, one by one.':^76}#")
        print(f"#{'Ensure each WorldEdit/server operation fully completes before proceeding.':^76}#")
        print(f"#{'':^76}#")
        print(f"#{'Transform your worlds, block by block!':^76}#")
        print(f"#{'':^76}#")
        print(f"#{'Let the building begin!':^76}#")
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
                if value_type == tuple and isinstance(default_value, tuple):
                    display_default_str = ','.join(map(str, default_value))
                else:
                    display_default_str = str(default_value)
                display_prompt += f" [{display_default_str}]"
            
            user_input = input(display_prompt + ": ").strip()

            if user_input == "":
                if default_value is not None:
                    if value_type == int:
                        return int(default_value)
                    elif value_type == tuple:
                        if isinstance(default_value, tuple):
                            return default_value
                        else:
                            parts = [int(p.strip()) for p in str(default_value).split(',')]
                            if len(parts) != 3:
                                 raise ValueError(f"Invalid default tuple format during conversion: {default_value}")
                            return tuple(parts)
                    return default_value
                else:
                    print("Input cannot be empty. Please provide a value.")
                    continue
            
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
            default_char = 'Y' if default_value else 'n'
            display_prompt += f" ({default_char}/n) [{default_char}]"
        else:
            display_prompt += " (Y/n)"

        user_input = input(display_prompt + ": ").strip().lower()

        if user_input == "":
            if default_value is not None:
                return default_value
            else:
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
            coords = [min(coords[0], coords[3]), min(coords[1], coords[4]), min(coords[2], coords[5]),
                      max(coords[0], coords[3]), max(coords[1], coords[4]), max(coords[2], coords[5])]
            boxes.append(tuple(coords))
            idx += 1
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
    
    if not boxes and not existing_boxes:
        print("No bounding boxes entered. Please enter at least one bounding box.")
        return get_bounding_boxes(existing_boxes) 
    elif not boxes and existing_boxes:
        return existing_boxes
    return boxes

def calculate_sub_regions(bbox, sub_region_size, target_origin_start):
    """
    Calculates sub-regions for a given bounding box and target origin.
    Returns a list of (source_bbox, target_paste_coords) tuples.
    Handles negative coordinates correctly.
    """
    x1, y1, z1, x2, y2, z2 = bbox
    
    dx = x2 - x1 + 1
    dy = y2 - y1 + 1
    dz = z2 - z1 + 1

    sub_regions = []

    for i_x in range(0, dx, sub_region_size):
        for i_z in range(0, dz, sub_region_size):
            src_sub_x1 = x1 + i_x
            src_sub_y1 = y1
            src_sub_z1 = z1 + i_z
            
            src_sub_x2 = min(x1 + i_x + sub_region_size - 1, x2)
            src_sub_y2 = y2
            src_sub_z2 = min(z1 + i_z + sub_region_size - 1, z2)

            target_paste_x = target_origin_start[0] + i_x
            target_paste_y = target_origin_start[1] 
            target_paste_z = target_origin_start[2] + i_z
            
            sub_regions.append(
                ((src_sub_x1, src_sub_y1, src_sub_z1, src_sub_x2, src_sub_y2, src_sub_z2),
                 (target_paste_x, target_paste_y, target_paste_z))
            )
    return sub_regions

def main():
    settings = {
        'source_world': None,
        'target_world': None,
        'creative_mode': None,
        'source_bounding_boxes': [],
        'target_paste_origin': None,
        'sub_region_size': None,
        'save_to_file': None,
        'output_filename': None,
        'mvtp_delay': None,
        'tp_delay': None,
        'copy_delay': None,
        'paste_delay': None,
        'generate_json': None,
        'json_filename': None, # This will be the *macro config file path* now
        'dry_run': None
    }
    
    initial_creative_mode_default = True
    initial_save_to_file_default = True
    initial_generate_json_default = True # Changed default to true
    initial_dry_run_default = True

    display_header(header_type="welcome")

    while True:
        if settings['source_world'] is None: # First run
            settings['source_world'] = get_input("Source World Name")
            settings['target_world'] = get_input("Target World Name")
            settings['creative_mode'] = get_yes_no_input("Creative Mode needed?", default_value=initial_creative_mode_default)
            settings['source_bounding_boxes'] = get_bounding_boxes()
            settings['target_paste_origin'] = get_input("Target Paste Origin (X,Y,Z)", default_value=(0,0,0), value_type=tuple)
            settings['sub_region_size'] = get_input("Sub-Region Size", default_value=64, value_type=int)
            settings['save_to_file'] = get_yes_no_input("Save plain text commands to a file?", default_value=initial_save_to_file_default)
            if settings['save_to_file']:
                settings['output_filename'] = get_input("Enter plain text filename (e.g., commands.txt)", default_value="commands.txt")

            settings['mvtp_delay'] = get_input("Delay *after* /mvtp (ticks)", default_value=20, value_type=int)
            settings['tp_delay'] = get_input("Delay *after* /tp (ticks)", default_value=15, value_type=int)
            settings['copy_delay'] = get_input("Delay *after* //copy (ticks)", default_value=50, value_type=int)
            settings['paste_delay'] = get_input("Delay *after* //paste (ticks)", default_value=100, value_type=int)

            settings['generate_json'] = get_yes_no_input("Generate Macro Mod profile JSON?", default_value=initial_generate_json_default)
            if settings['generate_json']:
                # Changed filename prompt to macro config path
                settings['json_filename'] = get_input("Enter path to Macro Mod config JSON file (e.g., .minecraft/macro/macros.json)", default_value=os.path.join(os.path.expanduser("~"), ".minecraft", "macro", "macros.json"))
            
            settings['dry_run'] = get_yes_no_input("Run in DRY-RUN mode (no actual //paste operations)?", default_value=initial_dry_run_default)


        else: # Re-prompt after 'n' confirmation
            display_header(header_type="restart")
            settings['source_world'] = get_input("Source World Name", default_value=settings['source_world'])
            settings['target_world'] = get_input("Target World Name", default_value=settings['target_world'])
            settings['creative_mode'] = get_yes_no_input("Creative Mode needed?", default_value=settings['creative_mode'])
            settings['source_bounding_boxes'] = get_bounding_boxes(existing_boxes=settings['source_bounding_boxes'])
            settings['target_paste_origin'] = get_input("Target Paste Origin (X,Y,Z)", default_value=settings['target_paste_origin'], value_type=tuple)
            settings['sub_region_size'] = get_input("Sub-Region Size", default_value=settings['sub_region_size'], value_type=int)
            settings['save_to_file'] = get_yes_no_input("Save plain text commands to a file?", default_value=settings['save_to_file'])
            if settings['save_to_file']:
                filename_default = settings['output_filename'] if settings['output_filename'] else "commands.txt"
                settings['output_filename'] = get_input("Enter plain text filename (e.g., commands.txt)", default_value=filename_default)
            else:
                settings['output_filename'] = None

            settings['mvtp_delay'] = get_input("Delay *after* /mvtp (ticks)", default_value=settings['mvtp_delay'], value_type=int)
            settings['tp_delay'] = get_input("Delay *after* /tp (ticks)", default_value=settings['tp_delay'], value_type=int)
            settings['copy_delay'] = get_input("Delay *after* //copy (ticks)", default_value=settings['copy_delay'], value_type=int)
            settings['paste_delay'] = get_input("Delay *after* //paste (ticks)", default_value=settings['paste_delay'], value_type=int)

            settings['generate_json'] = get_yes_no_input("Generate Macro Mod profile JSON?", default_value=settings['generate_json'])
            if settings['generate_json']:
                # Changed filename prompt to macro config path
                json_filename_default = settings['json_filename'] if settings['json_filename'] else os.path.join(os.path.expanduser("~"), ".minecraft", "macro", "macros.json")
                settings['json_filename'] = get_input("Enter path to Macro Mod config JSON file (e.g., .minecraft/macro/macros.json)", default_value=json_filename_default)
            else:
                settings['json_filename'] = None

            settings['dry_run'] = get_yes_no_input("Run in DRY-RUN mode (no actual //paste operations)?", default_value=settings['dry_run'])


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
        print(f"Target Paste Origin: ({settings['target_paste_origin'][0]}, {settings['target_paste_origin'][1]}, {settings['target_paste_origin'][2]})")
        print(f"Sub-Region Size: {settings['sub_region_size']}")
        print(f"Total Sub-Regions to Generate: {total_sub_regions}")
        
        if settings['save_to_file']:
            print(f"Save plain text commands to File: Yes (Filename: {settings['output_filename']})")
        else:
            print("Save plain text commands to File: No")

        if settings['generate_json']:
            print(f"Generate Macro Mod profile JSON: Yes (File: {settings['json_filename']})")
            print(f"  Delay *after* /mvtp: {settings['mvtp_delay']} ticks")
            print(f"  Delay *after* /tp: {settings['tp_delay']} ticks")
            print(f"  Delay *after* //copy: {settings['copy_delay']} ticks")
            print(f"  Delay *after* //paste: {settings['paste_delay']} ticks")
        else:
            print("Generate Macro Mod profile JSON: No")

        print(f"Dry-Run Mode: {'Yes (no actual //paste commands)' if settings['dry_run'] else 'No (will perform actual //paste commands)'}")

        print("#" * 60)
        print(f"#{'CAUTION: Large operations will be generated!':^58}#")
        print(f"#{'THIS IS YOUR LAST CHANCE TO REVIEW AND CONFIRM!':^58}#")
        print("#" * 60)

        confirm = get_yes_no_input("Proceed with command generation?")
        
        if confirm:
            break
        else:
            print("\nOkay, let's re-enter the details.")

    # --- Generate Commands ---
    display_header(header_type="generating")
    
    output_file_handle = None
    json_commands_list = [] # This will now be the 'messages' list for the new macro

    previous_command_type_for_delay = "none"

    def print_write_and_json(command_string, current_command_type="none"):
        nonlocal previous_command_type_for_delay

        print(command_string)

        if settings['save_to_file'] and output_file_handle:
            output_file_handle.write(command_string + '\n')

        # JSON generation logic (now populates json_commands_list)
        # Note: This list is built up and then added to the full macro profile later
        # It no longer directly writes a standalone JSON file.
        delay_for_this_json_entry = 0
        if previous_command_type_for_delay == "mvtp":
            delay_for_this_json_entry = settings['mvtp_delay']
        elif previous_command_type_for_delay == "tp":
            delay_for_this_json_entry = settings['tp_delay']
        elif previous_command_type_for_delay == "copy":
            delay_for_this_json_entry = settings['copy_delay']
        elif previous_command_type_for_delay == "paste":
            delay_for_this_json_entry = settings['paste_delay']
        
        json_string_to_add = command_string.strip() 
        if json_string_to_add.startswith("# --- SUB-REGION") or json_string_to_add == "":
            if json_string_to_add == "":
                json_string_to_add = "/say "
            else:
                json_string_to_add = f"/say {json_string_to_add}"
        # If it's already a /say command (like the dry run message), don't prepend /say again
        elif json_string_to_add.startswith("/say"):
            pass 
        # For other commands like /gamemode, /mvtp, //sel, //copy, //paste, they don't need /say prefix
        elif json_string_to_add.startswith("/"):
            pass
        # Fallback for any non-command strings that we might want to '/say'
        else:
            json_string_to_add = f"/say {json_string_to_add}"


        json_commands_list.append({
            "version": 1,
            "string": json_string_to_add,
            "delayTicks": delay_for_this_json_entry
        })

        previous_command_type_for_delay = current_command_type


    if settings['save_to_file']:
        try:
            output_file_handle = open(settings['output_filename'], 'w')
            print(f"Plain text commands will also be saved to '{settings['output_filename']}' in the current directory ({os.getcwd()})\n")
        except IOError as e:
            print(f"ERROR: Could not open plain text file '{settings['output_filename']}' for writing: {e}")
            print("Plain text commands will only be printed to console.")
            settings['save_to_file'] = False
            if output_file_handle:
                output_file_handle.close()

    sub_region_counter = 0
    for bbox_idx, bbox in enumerate(settings['source_bounding_boxes']):
        current_bbox_sub_regions = calculate_sub_regions(bbox, settings['sub_region_size'], settings['target_paste_origin'])
        
        for i, (src_coords, target_coords) in enumerate(current_bbox_sub_regions):
            sub_region_counter += 1
            print_write_and_json(f"# --- SUB-REGION {sub_region_counter} of {total_sub_regions} (Source: {src_coords[0]},{src_coords[1]},{src_coords[2]} to {src_coords[3]},{src_coords[4]},{src_coords[5]} -> Target: {target_coords[0]},{target_coords[1]},{target_coords[2]}) ---", "none")
            print_write_and_json(f"/mvtp {settings['source_world']}", "mvtp")
            print_write_and_json(f"/tp {src_coords[0]} {src_coords[1]} {src_coords[2]}", "tp")
            if settings['creative_mode']:
                print_write_and_json("/gamemode creative", "none")
            print_write_and_json(f"//pos1 {src_coords[0]},{src_coords[1]},{src_coords[2]}", "none")
            print_write_and_json(f"//pos2 {src_coords[3]},{src_coords[4]},{src_coords[5]}", "none")
            print_write_and_json(f"//copy -be", "copy")
            print_write_and_json(f"/mvtp {settings['target_world']}", "mvtp")
            print_write_and_json(f"/tp {target_coords[0]} {target_coords[1]} {target_coords[2]}", "tp")
            if settings['creative_mode']:
                print_write_and_json("/gamemode creative", "none")
            
            if settings['dry_run']:
                print_write_and_json(f"/say DRY RUN - Pasting from {src_coords[0]},{src_coords[1]},{src_coords[2]} to {target_coords[0]},{target_coords[1]},{target_coords[2]}", "paste")
            else:
                print_write_and_json(f"//paste -be", "paste")
            
            print_write_and_json("", "none") # Empty line for spacing

    print_write_and_json("/say WorldEdit transfer job complete! All regions processed.", "none")

    if output_file_handle:
        output_file_handle.close()
        print(f"\nAll plain text commands successfully saved to '{settings['output_filename']}'.")

    if settings['generate_json']:
        macro_config_path = settings['json_filename']
        macro_json_data = None

        # Load existing macro config
        try:
            # Ensure directory exists for new file or for reading
            os.makedirs(os.path.dirname(macro_config_path), exist_ok=True)
            with open(macro_config_path, 'r') as f:
                macro_json_data = json.load(f)
            print(f"Successfully loaded existing Macro Mod config from '{macro_config_path}'.")
        except FileNotFoundError:
            print(f"Macro Mod config file not found at '{macro_config_path}'. Creating a new skeletal config.")
            macro_json_data = {
                "version": 6,
                "profiles": [],
                "spDefault": 0,
                "mpDefault": 0,
                "defaultConflictStrategy": "SUBMIT",
                "defaultSendMode": "SEND",
                "defaultActivationType": "HOLD",
                "ratelimitCount": 4,
                "ratelimitTicks": 20,
                "ratelimitStrict": False,
                "ratelimitSp": False
            }
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in '{macro_config_path}': {e}. Please correct the file or choose a different path.")
            settings['generate_json'] = False # Disable JSON generation if file is corrupt
            macro_json_data = None # Prevent further processing

        if macro_json_data:
            # Generate profile name
            profile_name = f"{settings['source_world']} -> {settings['target_world']}"
            if settings['dry_run']:
                profile_name = f"DRY RUN: {profile_name}"

            # Create the new profile dictionary
            new_profile = {
                "version": 4,
                "name": profile_name,
                "links": [],
                "addToHistory": "OFF",
                "showHudMessage": "OFF",
                "resumeRepeating": "OFF",
                "useRatelimit": "ON",
                "macros": [
                    {
                        "version": 6,
                        "addToHistory": False,
                        "showHudMessage": False,
                        "resumeRepeating": False,
                        "useRatelimit": True,
                        "conflictStrategy": "SUBMIT",
                        "sendMode": "SEND",
                        "activationType": "VANILLA", # No keybind by default, triggerable by macro mod menu
                        "spaceTicks": 0,
                        "keybind": {
                            "version": 0,
                            "keyName": "key.keyboard.unknown",
                            "limitKeyName": "key.keyboard.unknown"
                        },
                        "altKeybind": {
                            "version": 0,
                            "keyName": "key.keyboard.unknown",
                            "limitKeyName": "key.keyboard.unknown"
                        },
                        "messages": json_commands_list # Our generated commands go here!
                    }
                ]
            }

            # Append new profile to the 'profiles' list
            if "profiles" not in macro_json_data:
                macro_json_data["profiles"] = []
            macro_json_data["profiles"].append(new_profile)

            # Save the updated JSON back to the file
            try:
                with open(macro_config_path, 'w') as f:
                    json.dump(macro_json_data, f, indent=2)
                print(f"Successfully added new profile '{profile_name}' to Macro Mod config at '{macro_config_path}'.")
            except IOError as e:
                print(f"ERROR: Could not write updated Macro Mod config to '{macro_config_path}': {e}")
            
    display_header(header_type="complete")

if __name__ == "__main__":
    main()