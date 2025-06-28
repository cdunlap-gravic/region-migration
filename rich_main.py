import math
import os
import json
import sys

# Rich Imports
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

# --- Global Rich Console ---
console = Console()

# --- Rich Styles Configuration ---
RICH_STYLES = {
    "rounded_orange": {
        "box_type": box.ROUNDED,
        "border_style": "orange1",
        "title_style": "bold orange_red1",
        "message_style": "dark_orange3",
        "align": "left"
    },
    "error_panel": { # Specific style for error panels
        "border_style": "red bold",
        "title_style": "bold white on red",
        "message_style": "red",
        "box_type": box.SQUARE,
        "align": "center"
    },
    "success_panel": { # Specific style for success panels
        "border_style": "green bold",
        "title_style": "bold white on green",
        "message_style": "green",
        "box_type": box.SQUARE,
        "align": "center"
    },
    "info_panel": { # Specific style for informational panels
        "border_style": "blue",
        "title_style": "bold blue",
        "message_style": "cyan",
        "box_type": box.SQUARE,
        "align": "left"
    },
    # Styles for direct text output (not panels)
    "plain_text": "default",
    "prompt": "bold white",
    "command_style": "bold yellow",
    "comment_style": "dim blue", # For comments like "--- SUB-REGION ---"
    "input_label": "bold cyan", # For the prompt label itself, e.g., "Source World Name"
    "default_value": "dim white", # For the default value in brackets
    "error_text": "red",
    "warning_text": "yellow"
}

# --- Configuration File Paths ---
SETTINGS_FILE = "settings.json"
JOBS_DIR = "jobs"

def display_header(header_type="default", title_override=None, message_override=None):
    """Displays a formatted header using Rich Panel based on the type."""
    style_config = RICH_STYLES["rounded_orange"] # Default to rounded orange
    title = ""
    message = ""
    width = 60 # Default width for panels

    if header_type == "welcome":
        title = "Minecraft WorldEdit Transfer Assistant"
        message = ("Welcome! This tool generates WorldEdit commands\n"
                   "to move structures between worlds.\n\n"
                   "Please provide the requested information below.")
        width = 70
    elif header_type == "review":
        title = "REVIEW YOUR INPUTS"
    elif header_type == "restart":
        title = "Restarting Input Process"
        message = "Let's try that again. Please re-enter the information.\nHit ENTER to keep the current value."
    elif header_type == "generating":
        title = "Generating your WorldEdit commands..."
        style_config = RICH_STYLES["info_panel"]
    elif header_type == "complete":
        title = "COMMAND GENERATION COMPLETE! YOUR ADVENTURE AWAITS!"
        message = ("Your comprehensive list of Minecraft WorldEdit commands is ready.\n\n"
                   "Copy them carefully and execute them in your Minecraft client, one by one.\n"
                   "Ensure each WorldEdit/server operation fully completes before proceeding.\n\n"
                   "Transform your worlds, block by block!\n\n"
                   "Let the building begin!")
        style_config = RICH_STYLES["success_panel"]
        width = 80
    elif header_type == "error":
        title = "ERROR"
        style_config = RICH_STYLES["error_panel"]
        message = message_override # Use message override for error text
    elif header_type == "warning":
        title = "WARNING"
        style_config = {"border_style": "yellow", "title_style": "bold yellow", "message_style": "yellow", "box_type": box.SQUARE}
        message = message_override


    if title_override:
        title = title_override
    if message_override and header_type not in ["error", "warning"]: # Error/warning use override as primary message
        message = message_override

    panel_content = Text(message, style=style_config["message_style"], justify="center") if message else ""

    console.print(
        Panel(
            panel_content,
            title=Text(title, style=style_config["title_style"], justify="center"),
            border_style=style_config["border_style"],
            box=style_config["box_type"],
            width=width,
            padding=(1, 2)
        )
    )

def get_input(prompt, default_value=None, value_type=str):
    """
    Prompts the user for input using rich console, showing a default value.
    Returns default_value (converted to value_type) if user hits Enter. Handles type conversion.
    """
    while True:
        try:
            display_prompt_text = Text(prompt, style=RICH_STYLES["input_label"])
            
            if default_value is not None:
                display_default_str = None
                if value_type == tuple and isinstance(default_value, tuple):
                    display_default_str = ','.join(map(str, default_value))
                else:
                    display_default_str = str(default_value)
                
                display_prompt_text.append(f" [{display_default_str}]", style=RICH_STYLES["default_value"])
            
            user_input = console.input(display_prompt_text + ": ").strip()

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
                                 console.print(f"[{RICH_STYLES['error_text']}]Invalid default tuple format during conversion: {default_value}[/{RICH_STYLES['error_text']}]")
                                 continue
                            return tuple(parts)
                    return default_value
                else:
                    console.print(f"[{RICH_STYLES['error_text']}]Input cannot be empty. Please provide a value.[/]")
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
            console.print(f"[{RICH_STYLES['error_text']}]Invalid input: {e}. Please try again.[/]")
        except Exception as e:
            console.print(f"[{RICH_STYLES['error_text']}]An unexpected error occurred: {e}. Please try again.[/]")

def get_yes_no_input(prompt, default_value=None):
    """
    Prompts for a yes/no input with validation and default handling using rich console.
    Returns True for 'yes', False for 'no'.
    """
    while True:
        display_prompt_text = Text(prompt, style=RICH_STYLES["input_label"])
        
        if default_value is not None:
            default_char = 'Y' if default_value else 'n'
            display_prompt_text.append(f" ({default_char}/n)", style=RICH_STYLES["default_value"])
            display_prompt_text.append(f" [{default_char}]", style=RICH_STYLES["default_value"])
        else:
            display_prompt_text.append(" (Y/n)", style=RICH_STYLES["default_value"])

        user_input = console.input(display_prompt_text + ": ").strip().lower()

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
            console.print(f"[{RICH_STYLES['error_text']}]Invalid response. Please enter 'y' or 'n'.[/]")

def get_bounding_boxes(existing_boxes=None):
    """
    Gets a list of bounding boxes from the user.
    Allows 'KEEP' to retain existing list during re-prompts.
    """
    boxes = []
    if existing_boxes:
        console.print(f"\n[{RICH_STYLES['plain_text']}]Current Source Bounding Boxes:[/]")
        for i, box in enumerate(existing_boxes):
            console.print(f"  [{RICH_STYLES['plain_text']}]{i+1}: ({box[0]},{box[1]},{box[2]}) to ({box[3]},{box[4]},{box[5]})[/]")
    
    console.print(f"[{RICH_STYLES['plain_text']}]Enter Source Bounding Boxes (X1,Y1,Z1,X2,Y2,Z2 format).[/]")
    console.print(f"[{RICH_STYLES['plain_text']}]Type 'DONE' when finished. Type 'KEEP' to retain current list.[/]")

    idx = 1
    while True:
        prompt_text = f"Enter Source Bounding Box #{idx} (or 'DONE' or 'KEEP')"
        user_input = console.input(f"[{RICH_STYLES['input_label']}]{prompt_text}: [/]").strip().upper()

        if user_input == 'DONE':
            break
        elif user_input == 'KEEP':
            if existing_boxes:
                return existing_boxes
            else:
                console.print(f"[{RICH_STYLES['error_text']}]Cannot 'KEEP' as no existing boxes are present. Please enter boxes or 'DONE'.[/]")
                continue
        
        try:
            coords = [int(p.strip()) for p in user_input.split(',')]
            if len(coords) != 6:
                raise ValueError("Bounding box must be X1,Y1,Z1,X2,Y2,Z2 (6 comma-separated numbers).")
            
            # Ensure coordinates are min/max for consistent internal representation
            coords = [min(coords[0], coords[3]), min(coords[1], coords[4]), min(coords[2], coords[5]),
                      max(coords[0], coords[3]), max(coords[1], coords[4]), max(coords[2], coords[5])]
            boxes.append(tuple(coords))
            idx += 1
        except ValueError as e:
            console.print(f"[{RICH_STYLES['error_text']}]Invalid input: {e}. Please try again.[/]")
    
    if not boxes and not existing_boxes:
        console.print(f"[{RICH_STYLES['error_text']}]No bounding boxes entered. Please enter at least one bounding box.[/]")
        return get_bounding_boxes(existing_boxes) 
    elif not boxes and existing_boxes: # If user typed DONE without new boxes but existing ones are present
        return existing_boxes
    return boxes

def calculate_sub_regions(bbox, sub_region_size, target_origin_start, overall_src_min_coords):
    """
    Calculates sub-regions for a given bounding box and target origin.
    Returns a list of (source_bbox, target_paste_coords) tuples.
    Uses overall_src_min_coords to maintain relative positioning across multiple bboxes.
    """
    x1, y1, z1, x2, y2, z2 = bbox
    
    # Calculate dimensions of the current bounding box
    dx = x2 - x1 + 1
    dy = y2 - y1 + 1 
    dz = z2 - z1 + 1

    overall_min_x, overall_min_y, overall_min_z = overall_src_min_coords

    sub_regions = []

    for i_x in range(0, dx, sub_region_size):
        for i_z in range(0, dz, sub_region_size):
            src_sub_x1 = x1 + i_x
            src_sub_y1 = y1 # Y-start of the current sub-region (same as bbox Y1)
            src_sub_z1 = z1 + i_z
            
            src_sub_x2 = min(x1 + i_x + sub_region_size - 1, x2)
            src_sub_y2 = y2 # Y-end of the current sub-region (same as bbox Y2)
            src_sub_z2 = min(z1 + i_z + sub_region_size - 1, z2)

            # Calculate target paste coords based on the overall structure's origin
            # Offset = (Current Sub-Region Start) - (Overall Structure Min)
            # Target Paste = (User Defined Target Origin) + Offset
            target_paste_x = target_origin_start[0] + (src_sub_x1 - overall_min_x)
            target_paste_y = target_origin_start[1] + (src_sub_y1 - overall_min_y) # Apply Y offset too!
            target_paste_z = target_origin_start[2] + (src_sub_z1 - overall_min_z)
            
            sub_regions.append(
                ((src_sub_x1, src_sub_y1, src_sub_z1, src_sub_x2, src_sub_y2, src_sub_z2),
                 (target_paste_x, target_paste_y, target_paste_z))
            )
    return sub_regions

def load_default_settings():
    """Loads default settings from SETTINGS_FILE."""
    defaults = {}
    try:
        with open(SETTINGS_FILE, 'r') as f:
            defaults = json.load(f)
        console.print(f"[{RICH_STYLES['plain_text']}]Loaded default settings from '{SETTINGS_FILE}'.[/]")
    except FileNotFoundError:
        console.print(f"[{RICH_STYLES['warning_text']}]'{SETTINGS_FILE}' not found. Using hardcoded defaults.[/]")
    except json.JSONDecodeError as e:
        console.print(f"[{RICH_STYLES['error_text']}]Error decoding '{SETTINGS_FILE}': {e}. Using hardcoded defaults.[/]")
    return defaults

def save_default_settings(current_settings):
    """Saves current relevant settings as new defaults to SETTINGS_FILE."""
    settings_to_save = {
        # Only save global defaults, not job-specific bounding boxes
        'source_world': current_settings.get('source_world'),
        'target_world': current_settings.get('target_world'),
        'creative_mode': current_settings.get('creative_mode'),
        # Convert tuple to list for JSON serialization
        'target_paste_origin': list(current_settings['target_paste_origin']) if current_settings.get('target_paste_origin') else None,
        'sub_region_size': current_settings.get('sub_region_size'),
        'save_to_file': current_settings.get('save_to_file'),
        'output_filename': current_settings.get('output_filename'),
        'mvtp_delay': current_settings.get('mvtp_delay'),
        'tp_delay': current_settings.get('tp_delay'),
        'copy_delay': current_settings.get('copy_delay'),
        'paste_delay': current_settings.get('paste_delay'),
        'generate_json': current_settings.get('generate_json'),
        'json_filename': current_settings.get('json_filename'),
        'dry_run': current_settings.get('dry_run')
    }
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings_to_save, f, indent=2)
        console.print(f"[{RICH_STYLES['plain_text']}]Current inputs saved as new default settings to '{SETTINGS_FILE}'.[/]")
    except IOError as e:
        console.print(f"[{RICH_STYLES['error_text']}]ERROR: Could not save default settings to '{SETTINGS_FILE}': {e}[/]")

def _ensure_jobs_dir_exists():
    """Ensures the JOBS_DIR exists."""
    os.makedirs(JOBS_DIR, exist_ok=True)

def list_available_jobs():
    """Lists available job files in the JOBS_DIR."""
    _ensure_jobs_dir_exists()
    jobs = []
    try:
        for filename in os.listdir(JOBS_DIR):
            if filename.endswith(".json"):
                jobs.append(filename[:-5]) # Remove .json extension
    except Exception as e:
        console.print(f"[{RICH_STYLES['error_text']}]Error listing jobs: {e}[/]")
    return jobs

def save_current_job(current_settings):
    """Prompts user for a job name and saves current settings to a job file."""
    _ensure_jobs_dir_exists()
    
    while True:
        job_name = console.input(f"[{RICH_STYLES['input_label']}]Enter a name for this job (e.g., 'MyBigBuildTransfer'): [/]").strip()
        if not job_name:
            console.print(f"[{RICH_STYLES['error_text']}]Job name cannot be empty. Please try again.[/]")
            continue
        
        job_file_path = os.path.join(JOBS_DIR, f"{job_name}.json")
        
        if os.path.exists(job_file_path):
            if not get_yes_no_input(f"Job '{job_name}' already exists. Overwrite?", default_value=False):
                console.print(f"[{RICH_STYLES['plain_text']}]Save cancelled. Please choose a different name or confirm overwrite.[/]")
                continue
        
        break # Valid name and overwrite decision made

    # Prepare settings for saving (convert tuples to lists)
    job_settings_to_save = current_settings.copy()
    if 'source_bounding_boxes' in job_settings_to_save and job_settings_to_save['source_bounding_boxes'] is not None:
        job_settings_to_save['source_bounding_boxes'] = [list(box) for box in job_settings_to_save['source_bounding_boxes']]
    else:
        job_settings_to_save['source_bounding_boxes'] = [] # Ensure it's saved as an empty list if not defined

    if 'target_paste_origin' in job_settings_to_save and job_settings_to_save['target_paste_origin'] is not None:
        job_settings_to_save['target_paste_origin'] = list(job_settings_to_save['target_paste_origin'])
    else:
        job_settings_to_save['target_paste_origin'] = [0,0,0] # Ensure it's saved as a default list if not defined

    # Remove temporary/dynamic keys if any that shouldn't be saved as part of the job
    job_settings_to_save.pop('output_file_handle', None) 
    job_settings_to_save.pop('json_commands_list', None)
    
    try:
        with open(job_file_path, 'w') as f:
            json.dump(job_settings_to_save, f, indent=2)
        console.print(f"[{RICH_STYLES['plain_text']}]Job '{job_name}' saved successfully to '{job_file_path}'.[/]")
    except IOError as e:
        console.print(f"[{RICH_STYLES['error_text']}]ERROR: Could not save job '{job_name}': {e}[/]")

def load_selected_job():
    """Prompts user to select and load an existing job."""
    available_jobs = list_available_jobs()
    if not available_jobs:
        console.print(f"[{RICH_STYLES['warning_text']}]No saved jobs found. Starting a new job instead.[/]")
        return None
    
    console.print(f"\n[{RICH_STYLES['plain_text']}]--- Available Jobs ---[/]")
    for i, job_name in enumerate(available_jobs):
        console.print(f"  [{RICH_STYLES['plain_text']}]{i+1}. {job_name}[/]")
    console.print(f"[{RICH_STYLES['plain_text']}]--------------------[/]")

    while True:
        try:
            choice = console.input(f"[{RICH_STYLES['input_label']}]Enter the number of the job to load, or 'C' to cancel: [/]").strip().lower()
            if choice == 'c':
                console.print(f"[{RICH_STYLES['plain_text']}]Job loading cancelled.[/]")
                return None
            
            job_idx = int(choice) - 1
            if 0 <= job_idx < len(available_jobs):
                job_name = available_jobs[job_idx]
                job_file_path = os.path.join(JOBS_DIR, f"{job_name}.json")
                
                with open(job_file_path, 'r') as f:
                    loaded_settings = json.load(f)
                
                # Convert lists back to tuples for bounding boxes and target origin
                if 'source_bounding_boxes' in loaded_settings and loaded_settings['source_bounding_boxes'] is not None:
                    loaded_settings['source_bounding_boxes'] = [tuple(box) for box in loaded_settings['source_bounding_boxes']]
                else:
                    loaded_settings['source_bounding_boxes'] = [] # Ensure it's a list if missing or null
                
                if 'target_paste_origin' in loaded_settings and loaded_settings['target_paste_origin'] is not None:
                    loaded_settings['target_paste_origin'] = tuple(loaded_settings['target_paste_origin'])
                else:
                    loaded_settings['target_paste_origin'] = (0,0,0) # Default if missing or null

                console.print(f"[{RICH_STYLES['plain_text']}]Job '{job_name}' loaded successfully.[/]")
                return loaded_settings

            else:
                console.print(f"[{RICH_STYLES['error_text']}]Invalid job number. Please try again.[/]")
        except ValueError:
            console.print(f"[{RICH_STYLES['error_text']}]Invalid input. Please enter a number or 'C'.[/]")
        except FileNotFoundError:
            console.print(f"[{RICH_STYLES['error_text']}]Error: Job file '{job_file_path}' not found. It might have been deleted.[/]")
            return None
        except json.JSONDecodeError as e:
            console.print(f"[{RICH_STYLES['error_text']}]Error decoding job file '{job_file_path}': {e}. The file might be corrupted.[/]")
            return None
        except Exception as e:
            console.print(f"[{RICH_STYLES['error_text']}]An unexpected error occurred while loading job: {e}[/]")
            return None

def main():
    # Ensure jobs directory exists
    _ensure_jobs_dir_exists()

    # Load default settings from settings.json
    loaded_defaults = load_default_settings()

    # Initialize settings with loaded defaults or hardcoded defaults
    settings = {
        'source_world': loaded_defaults.get('source_world'),
        'target_world': loaded_defaults.get('target_world'),
        'creative_mode': loaded_defaults.get('creative_mode', True),
        'source_bounding_boxes': [], # Always start fresh or load from job
        'target_paste_origin': tuple(loaded_defaults.get('target_paste_origin', (0,0,0))),
        'sub_region_size': loaded_defaults.get('sub_region_size', 64),
        'save_to_file': loaded_defaults.get('save_to_file', True),
        'output_filename': loaded_defaults.get('output_filename', "commands.txt"),
        'mvtp_delay': loaded_defaults.get('mvtp_delay', 20),
        'tp_delay': loaded_defaults.get('tp_delay', 15),
        'copy_delay': loaded_defaults.get('copy_delay', 50),
        'paste_delay': loaded_defaults.get('paste_delay', 100),
        'generate_json': loaded_defaults.get('generate_json', True),
        'json_filename': loaded_defaults.get('json_filename', os.path.join(os.path.expanduser("~"), ".minecraft", "macro", "macros.json")),
        'dry_run': loaded_defaults.get('dry_run', True)
    }
    
    display_header(header_type="welcome")

    # --- Initial Job Selection Loop ---
    job_selected = False
    while not job_selected:
        console.print(f"\n[{RICH_STYLES['plain_text']}]What would you like to do?[/]")
        console.print(f"  [{RICH_STYLES['plain_text']}]1. Start a New Transfer Job[/]")
        console.print(f"  [{RICH_STYLES['plain_text']}]2. Load an Existing Transfer Job[/]")
        console.print(f"  [{RICH_STYLES['plain_text']}]3. Exit[/]")
        choice = console.input(f"[{RICH_STYLES['input_label']}]Enter your choice (1, 2, or 3): [/]").strip()

        if choice == '1':
            job_selected = True
        elif choice == '2':
            loaded_job_settings = load_selected_job()
            if loaded_job_settings:
                settings.update(loaded_job_settings) # Overwrite current settings with loaded job
                job_selected = True
            else:
                # If load failed or cancelled, loop back to the menu
                continue
        elif choice == '3':
            console.print(f"[{RICH_STYLES['plain_text']}]Exiting. Goodbye![/]")
            sys.exit()
        else:
            console.print(f"[{RICH_STYLES['error_text']}]Invalid choice. Please enter 1, 2, or 3.[/]")

    # --- Input Gathering / Review Loop ---
    input_phase_complete = False
    while not input_phase_complete:
        if choice == '1': # Only prompt inputs if starting a new job (or load failed/cancelled)
            console.print(f"\n[{RICH_STYLES['plain_text']}]Please provide the details for your new transfer job.[/]")
            settings['source_world'] = get_input("Source World Name", default_value=settings['source_world'])
            settings['target_world'] = get_input("Target World Name", default_value=settings['target_world'])
            settings['creative_mode'] = get_yes_no_input("Creative Mode needed?", default_value=settings['creative_mode'])
            
            settings['source_bounding_boxes'] = get_bounding_boxes(existing_boxes=settings['source_bounding_boxes'])
            
            settings['target_paste_origin'] = get_input("Target Paste Origin (X,Y,Z)", default_value=settings['target_paste_origin'], value_type=tuple)
            settings['sub_region_size'] = get_input("Sub-Region Size", default_value=settings['sub_region_size'], value_type=int)
            settings['save_to_file'] = get_yes_no_input("Save plain text commands to a file?", default_value=settings['save_to_file'])
            if settings['save_to_file']:
                settings['output_filename'] = get_input("Enter plain text filename (e.g., commands.txt)", default_value=settings['output_filename'])
            else:
                settings['output_filename'] = None

            settings['mvtp_delay'] = get_input("Delay *after* /mvtp (ticks)", default_value=settings['mvtp_delay'], value_type=int)
            settings['tp_delay'] = get_input("Delay *after* /tp (ticks)", default_value=settings['tp_delay'], value_type=int)
            settings['copy_delay'] = get_input("Delay *after* //copy (ticks)", default_value=settings['copy_delay'], value_type=int)
            settings['paste_delay'] = get_input("Delay *after* //paste (ticks)", default_value=settings['paste_delay'], value_type=int)

            settings['generate_json'] = get_yes_no_input("Generate Macro Mod profile JSON?", default_value=settings['generate_json'])
            if settings['generate_json']:
                settings['json_filename'] = get_input("Enter path to Macro Mod config JSON file (e.g., .minecraft/macro/macros.json)", default_value=settings['json_filename'])
            else:
                settings['json_filename'] = None
            
            settings['dry_run'] = get_yes_no_input("Run in DRY-RUN mode (no actual //paste operations)?", default_value=settings['dry_run'])

        # --- Calculate overall min/max for all source bounding boxes ---
        overall_src_min_coords = (0,0,0) # Default if no boxes, though get_bounding_boxes ensures at least one

        if settings['source_bounding_boxes']:
            # Initialize with values from the first bbox
            overall_min_x = settings['source_bounding_boxes'][0][0]
            overall_min_y = settings['source_bounding_boxes'][0][1]
            overall_min_z = settings['source_bounding_boxes'][0][2]
            
            # Iterate through all bounding boxes to find the true overall min/max
            for bbox in settings['source_bounding_boxes']: 
                overall_min_x = min(overall_min_x, bbox[0])
                overall_min_y = min(overall_min_y, bbox[1])
                overall_min_z = min(overall_min_z, bbox[2])
            
            overall_src_min_coords = (overall_min_x, overall_min_y, overall_min_z)

        # Generate sub-regions using the new overall_src_min_coords
        all_sub_regions = []
        for bbox in settings['source_bounding_boxes']:
            # Pass the overall_src_min_coords to calculate_sub_regions
            all_sub_regions.extend(calculate_sub_regions(bbox, settings['sub_region_size'], settings['target_paste_origin'], overall_src_min_coords))
        
        total_sub_regions = len(all_sub_regions)

        # --- Review and Confirm ---
        display_header(header_type="review")
        console.print(f"[{RICH_STYLES['plain_text']}]Source World: {settings['source_world']}[/]")
        console.print(f"[{RICH_STYLES['plain_text']}]Target World: {settings['target_world']}[/]")
        console.print(f"[{RICH_STYLES['plain_text']}]Set Gamemode to Creative: {'Yes' if settings['creative_mode'] else 'No'}[/]")
        console.print(f"[{RICH_STYLES['plain_text']}]Source Bounding Boxes:[/]")
        for i, box in enumerate(settings['source_bounding_boxes']):
            console.print(f"  [{RICH_STYLES['plain_text']}]Box {i+1}: ({box[0]}, {box[1]}, {box[2]}) to ({box[3]}, {box[4]}, {box[5]})[/]")
        console.print(f"[{RICH_STYLES['plain_text']}]Overall Source Min Coords (Anchor): ({overall_src_min_coords[0]}, {overall_src_min_coords[1]}, {overall_src_min_coords[2]})[/]")
        console.print(f"[{RICH_STYLES['plain_text']}]Target Paste Origin: ({settings['target_paste_origin'][0]}, {settings['target_paste_origin'][1]}, {settings['target_paste_origin'][2]})[/]")
        console.print(f"[{RICH_STYLES['plain_text']}]Sub-Region Size: {settings['sub_region_size']}[/]")
        console.print(f"[{RICH_STYLES['plain_text']}]Total Sub-Regions to Generate: {total_sub_regions}[/]")
        
        if settings['save_to_file']:
            console.print(f"[{RICH_STYLES['plain_text']}]Save plain text commands to File: Yes (Filename: {settings['output_filename']})[/]")
        else:
            console.print(f"[{RICH_STYLES['plain_text']}]Save plain text commands to File: No[/]")

        if settings['generate_json']:
            console.print(f"[{RICH_STYLES['plain_text']}]Generate Macro Mod profile JSON: Yes (File: {settings['json_filename']})[/]")
            console.print(f"  [{RICH_STYLES['plain_text']}]Delay *after* /mvtp: {settings['mvtp_delay']} ticks[/]")
            console.print(f"  [{RICH_STYLES['plain_text']}]Delay *after* /tp: {settings['tp_delay']} ticks[/]")
            console.print(f"  [{RICH_STYLES['plain_text']}]Delay *after* //copy: {settings['copy_delay']} ticks[/]")
            console.print(f"  [{RICH_STYLES['plain_text']}]Delay *after* //paste: {settings['paste_delay']} ticks[/]")
        else:
            console.print(f"[{RICH_STYLES['plain_text']}]Generate Macro Mod profile JSON: No[/]")

        console.print(f"[{RICH_STYLES['plain_text']}]Dry-Run Mode: {'Yes (no actual //paste commands)' if settings['dry_run'] else 'No (will perform actual //paste commands)'}[/]")

        console.print(f"[{RICH_STYLES['warning_text']}]" + "#" * 60)
        console.print(f"[{RICH_STYLES['warning_text']}]{'CAUTION: Large operations will be generated!':^58}")
        console.print(f"[{RICH_STYLES['warning_text']}]{'THIS IS YOUR LAST CHANCE TO REVIEW AND CONFIRM!':^58}")
        console.print(f"[{RICH_STYLES['warning_text']}]" + "#" * 60 + "[/]")

        confirm = get_yes_no_input("Proceed with command generation?")
        
        if confirm:
            input_phase_complete = True
        else:
            console.print(f"\n[{RICH_STYLES['plain_text']}]Okay, let's re-enter the details.[/]")
            display_header(header_type="restart")
            choice = '1' # Set choice back to '1' to re-enter inputs on next loop iteration

    # --- Generate Commands ---
    display_header(header_type="generating")
    
    output_file_handle = None
    json_commands_list = [] # This will now be the 'messages' list for the new macro

    previous_command_type_for_delay = "none"

    def print_write_and_json(command_string, command_category="none", is_comment=False):
        nonlocal previous_command_type_for_delay

        # --- Console Output ---
        if is_comment:
            console.print(Text(command_string, style=RICH_STYLES["comment_style"]))
        elif command_string:
            console.print(Text(command_string, style=RICH_STYLES["command_style"]))
        else: # Empty string, for visual spacing in console only
            console.print("")

        # --- File Output (plain text) ---
        # Only write if the command_string is not empty AND it's not purely a comment
        if settings['save_to_file'] and output_file_handle and command_string and not is_comment:
            output_file_handle.write(command_string + '\n')

        # --- JSON Output (Macro Mod) ---
        # Only add to JSON list if the command_string is not empty and not purely a comment
        if settings['generate_json'] and command_string:
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
            
            # For JSON, if it's not a command (starts with /), convert to /say for macro mod
            # This applies to comments (like # --- SUB-REGION...) too, converting them to /say commands
            if not json_string_to_add.startswith("/"):
                json_string_to_add = f"/say {json_string_to_add}"

            json_commands_list.append({
                "version": 1,
                "string": json_string_to_add,
                "delayTicks": delay_for_this_json_entry
            })

        # Update previous command type *only if it was an actual command category*
        if command_category in ["mvtp", "tp", "copy", "paste"]:
             previous_command_type_for_delay = command_category
        # If it was a comment or a non-delay type, previous_command_type_for_delay remains unchanged
        # This ensures delay is applied correctly to the *next* real command.


    if settings['save_to_file']:
        try:
            output_file_handle = open(settings['output_filename'], 'w')
            console.print(f"[{RICH_STYLES['plain_text']}]\nPlain text commands will also be saved to '{settings['output_filename']}' in the current directory ({os.getcwd()})\n[/]")
        except IOError as e:
            console.print(f"[{RICH_STYLES['error_text']}]ERROR: Could not open plain text file '{settings['output_filename']}' for writing: {e}[/]")
            console.print(f"[{RICH_STYLES['plain_text']}]Plain text commands will only be printed to console.[/]")
            settings['save_to_file'] = False
            if output_file_handle:
                output_file_handle.close()

    sub_region_counter = 0
    for i, (src_coords, target_coords) in enumerate(all_sub_regions):
        sub_region_counter += 1
        print_write_and_json(f"# --- SUB-REGION {sub_region_counter} of {total_sub_regions} (Source: {src_coords[0]},{src_coords[1]},{src_coords[2]} to {src_coords[3]},{src_coords[4]},{src_coords[5]} -> Target: {target_coords[0]},{target_coords[1]},{target_coords[2]}) ---", is_comment=True)
        print_write_and_json(f"/mvtp {settings['source_world']}", "mvtp")
        print_write_and_json(f"/tp {src_coords[0]} {src_coords[1]} {src_coords[2]}", "tp")
        if settings['creative_mode']:
            print_write_and_json("/gamemode creative", "none") # No delay category
        
        print_write_and_json(f"//pos1 {src_coords[0]},{src_coords[1]},{src_coords[2]}", "none") # No delay category
        print_write_and_json(f"//pos2 {src_coords[3]},{src_coords[4]},{src_coords[5]}", "none") # No delay category

        print_write_and_json(f"//copy -be", "copy")
        print_write_and_json(f"/mvtp {settings['target_world']}", "mvtp")
        print_write_and_json(f"/tp {target_coords[0]} {target_coords[1]} {target_coords[2]}", "tp")
        if settings['creative_mode']:
            print_write_and_json("/gamemode creative", "none") # No delay category
        
        if settings['dry_run']:
            print_write_and_json(f"/say DRY RUN - Pasting from {src_coords[0]},{src_coords[1]},{src_coords[2]} to {target_coords[0]},{target_coords[1]},{target_coords[2]}", "paste")
        else:
            print_write_and_json(f"//paste -be", "paste")
        
        console.print("") # Print empty line for console spacing ONLY, without creating a command

    print_write_and_json("/say WorldEdit transfer job complete! All regions processed.", is_comment=True)

    if output_file_handle:
        output_file_handle.close()
        console.print(f"\n[{RICH_STYLES['plain_text']}]All plain text commands successfully saved to '{settings['output_filename']}'.[/]")

    if settings['generate_json']:
        macro_config_path = settings['json_filename']
        macro_json_data = None

        try:
            os.makedirs(os.path.dirname(macro_config_path), exist_ok=True)
            with open(macro_config_path, 'r') as f:
                macro_json_data = json.load(f)
            console.print(f"[{RICH_STYLES['plain_text']}]Successfully loaded existing Macro Mod config from '{macro_config_path}'.[/]")
        except FileNotFoundError:
            console.print(f"[{RICH_STYLES['warning_text']}]Macro Mod config file not found at '{macro_config_path}'. Creating a new skeletal config.[/]")
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
            console.print(f"[{RICH_STYLES['error_text']}]ERROR: Invalid JSON in '{macro_config_path}': {e}. Please correct the file or choose a different path.[/]")
            settings['generate_json'] = False
            macro_json_data = None

        if macro_json_data:
            profile_name = f"{settings['source_world']} -> {settings['target_world']}"
            if settings['dry_run']:
                profile_name = f"DRY RUN: {profile_name}"

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
                        "activationType": "VANILLA",
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
                        "messages": json_commands_list
                    }
                ]
            }

            if "profiles" not in macro_json_data:
                macro_json_data["profiles"] = []
            
            # Check if a profile with the same name already exists and replace it
            profile_exists = False
            for i, profile in enumerate(macro_json_data["profiles"]):
                if profile.get("name") == profile_name:
                    macro_json_data["profiles"][i] = new_profile
                    profile_exists = True
                    console.print(f"[{RICH_STYLES['plain_text']}]Replaced existing Macro Mod profile '{profile_name}'.[/]")
                    break
            
            if not profile_exists:
                macro_json_data["profiles"].append(new_profile)
                console.print(f"[{RICH_STYLES['plain_text']}]Successfully added new Macro Mod profile '{profile_name}' to config at '{macro_config_path}'.[/]")

            try:
                with open(macro_config_path, 'w') as f:
                    json.dump(macro_json_data, f, indent=2)
            except IOError as e:
                console.print(f"[{RICH_STYLES['error_text']}]ERROR: Could not write updated Macro Mod config to '{macro_config_path}': {e}[/]")
            
    display_header(header_type="complete")

    # --- Save Default Settings ---
    if get_yes_no_input("Do you want to save these settings as new defaults for future runs?", default_value=True):
        save_default_settings(settings)
    
    # --- Save Current Job ---
    if get_yes_no_input("Do you want to save this specific job for future use?", default_value=False):
        save_current_job(settings)


if __name__ == "__main__":
    main()