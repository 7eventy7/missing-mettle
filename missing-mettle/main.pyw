import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import threading
import os
import time
from typing import Dict, List, Set

class TF2WeaponChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Missing Mettle")
        self.root.geometry("1920x1080")
        
        self.setup_dark_theme()
        
        self.all_weapons = []
        self.user_weapons = set()
        self.filtered_missing_weapons = []
        self.obtained_weapons = []
        
        self.class_names = {
            0: "0: Multiclass", 1: "1: Scout", 2: "2: Soldier", 3: "3: Pyro", 
            4: "4: Demoman", 5: "5: Heavy", 6: "6: Engineer", 7: "7: Medic", 
            8: "8: Sniper", 9: "9: Spy"
        }
        
        self.slot_names = {
            1: "1: Primary", 2: "2: Secondary", 3: "3: Melee", 4: "4: Special"
        }
        
        self.class_filters = {}
        self.slot_filters = {}
        self.type_filters = {}
        
        self.setup_ui()
        
    def setup_dark_theme(self):
        self.colors = {
            'bg_primary': '#1e1e1e',
            'bg_secondary': '#2d2d2d',
            'bg_tertiary': '#3c3c3c',
            'bg_hover': '#4a4a4a',
            'bg_selected': '#0d7377',
            'fg_primary': '#ffffff',
            'fg_secondary': '#cccccc',
            'fg_disabled': '#666666',
            'border': '#555555',
            'accent': '#00a8cc'
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TLabel', 
                       background=self.colors['bg_primary'], 
                       foreground=self.colors['fg_primary'],
                       font=('Segoe UI', 9))
        
        style.configure('TFrame', 
                       background=self.colors['bg_primary'],
                       borderwidth=0)
        
        style.configure('TLabelFrame', 
                       background=self.colors['bg_primary'], 
                       foreground=self.colors['fg_primary'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['border'])
        
        style.configure('TLabelFrame.Label', 
                       background=self.colors['bg_primary'], 
                       foreground=self.colors['fg_primary'],
                       font=('Segoe UI', 9, 'bold'))
        
        style.configure('TButton', 
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['fg_primary'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['border'],
                       focuscolor='none',
                       font=('Segoe UI', 9))
        
        style.map('TButton', 
                 background=[('active', self.colors['bg_hover']),
                           ('pressed', self.colors['bg_selected'])],
                 bordercolor=[('active', self.colors['accent']),
                            ('pressed', self.colors['accent'])])
        
        style.configure('TEntry', 
                       fieldbackground=self.colors['bg_tertiary'],
                       foreground=self.colors['fg_primary'],
                       borderwidth=1,
                       bordercolor=self.colors['border'],
                       lightcolor=self.colors['border'],
                       darkcolor=self.colors['border'],
                       insertcolor=self.colors['fg_primary'],
                       relief='solid',
                       font=('Segoe UI', 9))
        
        style.map('TEntry',
                 fieldbackground=[('focus', self.colors['bg_hover'])],
                 bordercolor=[('focus', self.colors['accent'])])
        
        style.configure('TCheckbutton', 
                       background=self.colors['bg_primary'],
                       foreground=self.colors['fg_primary'],
                       focuscolor='none',
                       font=('Segoe UI', 9))
        
        style.map('TCheckbutton', 
                 background=[('active', self.colors['bg_primary'])],
                 foreground=[('active', self.colors['fg_primary'])])
        
        style.configure('Treeview', 
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['fg_primary'],
                       fieldbackground=self.colors['bg_secondary'],
                       borderwidth=1,
                       bordercolor=self.colors['border'],
                       relief='solid',
                       font=('Segoe UI', 9))
        
        style.configure('Treeview.Heading', 
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['fg_primary'],
                       borderwidth=1,
                       bordercolor=self.colors['border'],
                       relief='solid',
                       font=('Segoe UI', 9, 'bold'))
        
        style.map('Treeview', 
                 background=[('selected', self.colors['bg_selected'])],
                 foreground=[('selected', self.colors['fg_primary'])])
        
        style.map('Treeview.Heading', 
                 background=[('active', self.colors['bg_hover'])])
        
        style.configure('Vertical.TScrollbar',
                       background=self.colors['bg_tertiary'],
                       bordercolor=self.colors['border'],
                       arrowcolor=self.colors['fg_secondary'],
                       darkcolor=self.colors['bg_tertiary'],
                       lightcolor=self.colors['bg_tertiary'])
        
        style.map('Vertical.TScrollbar',
                 background=[('active', self.colors['bg_hover'])])
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'], padx=10, pady=10)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        title_label = tk.Label(main_frame, text="Missing Mettle", 
                              bg=self.colors['bg_primary'], fg=self.colors['fg_primary'],
                              font=("Segoe UI", 30, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        input_container = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        input_container.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_container.columnconfigure(0, weight=1)
        
        input_header = tk.Label(input_container, text="Setup", 
                               bg=self.colors['bg_primary'], fg=self.colors['fg_primary'],
                               font=("Segoe UI", 10, "bold"))
        input_header.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        input_frame = tk.Frame(input_container, bg=self.colors['bg_secondary'], 
                              relief='solid', bd=1, highlightbackground=self.colors['border'])
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=0, pady=0)
        input_frame.columnconfigure(1, weight=1)
        
        for i in range(4):
            input_frame.grid_rowconfigure(i, pad=5)
        for i in range(2):
            input_frame.grid_columnconfigure(i, pad=10)
        
        api_label = tk.Label(input_frame, text="Steam API Key:", 
                            bg=self.colors['bg_secondary'], fg=self.colors['fg_primary'],
                            font=('Segoe UI', 9))
        api_label.grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        
        self.api_key_var = tk.StringVar()
        api_entry = tk.Entry(input_frame, textvariable=self.api_key_var, show="*", width=50,
                            bg=self.colors['bg_tertiary'], fg=self.colors['fg_primary'],
                            insertbackground=self.colors['fg_primary'], font=('Segoe UI', 9),
                            relief='solid', bd=1, highlightbackground=self.colors['border'])
        api_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 10), pady=10)
        
        steam_label = tk.Label(input_frame, text="Steam ID/URL:", 
                              bg=self.colors['bg_secondary'], fg=self.colors['fg_primary'],
                              font=('Segoe UI', 9))
        steam_label.grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        
        self.steam_id_var = tk.StringVar()
        steam_entry = tk.Entry(input_frame, textvariable=self.steam_id_var, width=50,
                              bg=self.colors['bg_tertiary'], fg=self.colors['fg_primary'],
                              insertbackground=self.colors['fg_primary'], font=('Segoe UI', 9),
                              relief='solid', bd=1, highlightbackground=self.colors['border'])
        steam_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 10), pady=10)
        
        help_label = tk.Label(input_frame, text="(SteamID64, custom URL, or profile URL)", 
                             bg=self.colors['bg_secondary'], fg=self.colors['fg_secondary'],
                             font=("Segoe UI", 8))
        help_label.grid(row=2, column=1, sticky=tk.W, padx=(5, 10))
        
        check_btn = tk.Button(input_frame, text="Check Missing Weapons", 
                             bg=self.colors['bg_tertiary'], fg=self.colors['fg_primary'],
                             font=('Segoe UI', 9), relief='solid', bd=1,
                             highlightbackground=self.colors['border'],
                             activebackground=self.colors['bg_hover'],
                             command=self.check_weapons)
        check_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        content_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        content_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(1, weight=1)
        content_frame.columnconfigure(2, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        filters_container = tk.Frame(content_frame, bg=self.colors['bg_primary'])
        filters_container.grid(row=0, column=0, sticky=(tk.W, tk.N, tk.S), padx=(0, 10))
        
        filters_header = tk.Label(filters_container, text="Filters", 
                                 bg=self.colors['bg_primary'], fg=self.colors['fg_primary'],
                                 font=("Segoe UI", 10, "bold"))
        filters_header.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        filters_frame = tk.Frame(filters_container, bg=self.colors['bg_secondary'], 
                                relief='solid', bd=1, highlightbackground=self.colors['border'])
        filters_frame.grid(row=1, column=0, sticky=(tk.W, tk.N, tk.S), padx=0, pady=0)
        
        self.setup_filters(filters_frame)
        
        missing_container = tk.Frame(content_frame, bg=self.colors['bg_primary'])
        missing_container.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        missing_container.columnconfigure(0, weight=1)
        missing_container.rowconfigure(1, weight=1)
        
        missing_header = tk.Label(missing_container, text="Missing Weapons", 
                                 bg=self.colors['bg_primary'], fg=self.colors['fg_primary'],
                                 font=("Segoe UI", 10, "bold"))
        missing_header.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        missing_frame = tk.Frame(missing_container, bg=self.colors['bg_secondary'], 
                                relief='solid', bd=1, highlightbackground=self.colors['border'])
        missing_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=0, pady=0)
        missing_frame.columnconfigure(0, weight=1)
        missing_frame.rowconfigure(0, weight=1)
        
        columns = ('name', 'class', 'slot', 'tier', 'type', 'tag')
        self.missing_tree = ttk.Treeview(missing_frame, columns=columns, show='headings', height=15)
        
        self.missing_tree.heading('name', text='Weapon Name')
        self.missing_tree.heading('class', text='Class')
        self.missing_tree.heading('slot', text='Slot')
        self.missing_tree.heading('tier', text='Tier')
        self.missing_tree.heading('type', text='Type')
        self.missing_tree.heading('tag', text='Tag')
        
        self.missing_tree.column('name', width=200)
        self.missing_tree.column('class', width=100)
        self.missing_tree.column('slot', width=80)
        self.missing_tree.column('tier', width=80)
        self.missing_tree.column('type', width=80)
        self.missing_tree.column('tag', width=80)
        
        missing_scrollbar = ttk.Scrollbar(missing_frame, orient=tk.VERTICAL, command=self.missing_tree.yview)
        self.missing_tree.configure(yscrollcommand=missing_scrollbar.set)
        
        self.missing_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        missing_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        obtained_container = tk.Frame(content_frame, bg=self.colors['bg_primary'])
        obtained_container.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        obtained_container.columnconfigure(0, weight=1)
        obtained_container.rowconfigure(1, weight=1)
        
        obtained_header = tk.Label(obtained_container, text="Obtained Weapons", 
                                  bg=self.colors['bg_primary'], fg=self.colors['fg_primary'],
                                  font=("Segoe UI", 10, "bold"))
        obtained_header.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        obtained_frame = tk.Frame(obtained_container, bg=self.colors['bg_secondary'], 
                                 relief='solid', bd=1, highlightbackground=self.colors['border'])
        obtained_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=0, pady=0)
        obtained_frame.columnconfigure(0, weight=1)
        obtained_frame.rowconfigure(0, weight=1)
        
        self.obtained_tree = ttk.Treeview(obtained_frame, columns=columns, show='headings', height=15)
        
        self.obtained_tree.heading('name', text='Weapon Name')
        self.obtained_tree.heading('class', text='Class')
        self.obtained_tree.heading('slot', text='Slot')
        self.obtained_tree.heading('tier', text='Tier')
        self.obtained_tree.heading('type', text='Type')
        self.obtained_tree.heading('tag', text='Tag')
        
        self.obtained_tree.column('name', width=200)
        self.obtained_tree.column('class', width=100)
        self.obtained_tree.column('slot', width=80)
        self.obtained_tree.column('tier', width=80)
        self.obtained_tree.column('type', width=80)
        self.obtained_tree.column('tag', width=80)
        
        obtained_scrollbar = ttk.Scrollbar(obtained_frame, orient=tk.VERTICAL, command=self.obtained_tree.yview)
        self.obtained_tree.configure(yscrollcommand=obtained_scrollbar.set)
        
        self.obtained_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        obtained_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.status_var = tk.StringVar(value="Ready")
        status_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'], 
                               height=25, relief='solid', bd=1)
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.grid_propagate(False)
        
        status_label = tk.Label(status_frame, textvariable=self.status_var,
                               bg=self.colors['bg_secondary'], fg=self.colors['fg_primary'],
                               font=('Segoe UI', 9), anchor='w')
        status_label.pack(fill=tk.BOTH, expand=True, padx=5)
    
    def setup_filters(self, parent):
        row = 0
        
        parent.configure(padx=10, pady=10)
        
        class_label = tk.Label(parent, text="Classes:", 
                              bg=self.colors['bg_secondary'], fg=self.colors['fg_primary'],
                              font=("Segoe UI", 10, "bold"))
        class_label.grid(row=row, column=0, sticky=tk.W, pady=(5, 5))
        row += 1
        
        for class_id, class_name in self.class_names.items():
            var = tk.BooleanVar(value=True)
            self.class_filters[class_id] = var
            cb = tk.Checkbutton(parent, text=class_name, variable=var, 
                               bg=self.colors['bg_secondary'], fg=self.colors['fg_primary'],
                               selectcolor=self.colors['bg_tertiary'], font=('Segoe UI', 9),
                               activebackground=self.colors['bg_secondary'],
                               activeforeground=self.colors['fg_primary'],
                               highlightthickness=0,
                               command=self.apply_filters)
            cb.grid(row=row, column=0, sticky=tk.W, pady=1)
            row += 1
        
        row += 1
        
        slot_label = tk.Label(parent, text="Slots:", 
                             bg=self.colors['bg_secondary'], fg=self.colors['fg_primary'],
                             font=("Segoe UI", 10, "bold"))
        slot_label.grid(row=row, column=0, sticky=tk.W, pady=(5, 5))
        row += 1
        
        for slot_id, slot_name in self.slot_names.items():
            var = tk.BooleanVar(value=True)
            self.slot_filters[slot_id] = var
            cb = tk.Checkbutton(parent, text=slot_name, variable=var,
                               bg=self.colors['bg_secondary'], fg=self.colors['fg_primary'],
                               selectcolor=self.colors['bg_tertiary'], font=('Segoe UI', 9),
                               activebackground=self.colors['bg_secondary'],
                               activeforeground=self.colors['fg_primary'],
                               highlightthickness=0,
                               command=self.apply_filters)
            cb.grid(row=row, column=0, sticky=tk.W, pady=1)
            row += 1
        
        row += 1
        
        type_label = tk.Label(parent, text="Types:", 
                             bg=self.colors['bg_secondary'], fg=self.colors['fg_primary'],
                             font=("Segoe UI", 10, "bold"))
        type_label.grid(row=row, column=0, sticky=tk.W, pady=(5, 5))
        row += 1
        
        for weapon_type in ["Normal", "Reskin"]:
            var = tk.BooleanVar(value=True)
            self.type_filters[weapon_type] = var
            cb = tk.Checkbutton(parent, text=weapon_type, variable=var,
                               bg=self.colors['bg_secondary'], fg=self.colors['fg_primary'],
                               selectcolor=self.colors['bg_tertiary'], font=('Segoe UI', 9),
                               activebackground=self.colors['bg_secondary'],
                               activeforeground=self.colors['fg_primary'],
                               highlightthickness=0,
                               command=self.apply_filters)
            cb.grid(row=row, column=0, sticky=tk.W, pady=1)
            row += 1
    
    def load_weapons_data(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(script_dir, "list.json")
            
            if not os.path.exists(json_path):
                messagebox.showerror("Error", f"list.json not found in {script_dir}")
                return False
                
            with open(json_path, 'r', encoding='utf-8') as f:
                self.all_weapons = json.load(f)
            
            self.status_var.set(f"Loaded {len(self.all_weapons)} weapons from list.json")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load list.json: {str(e)}")
            return False
    
    def resolve_steam_id(self, steam_input, api_key):
        steam_input = steam_input.strip()
        
        if steam_input.isdigit() and len(steam_input) == 17 and steam_input.startswith('7656119'):
            return steam_input
        
        if 'steamcommunity.com/profiles/' in steam_input:
            steam_id = steam_input.split('/profiles/')[-1].split('/')[0]
            if steam_id.isdigit() and len(steam_id) == 17:
                return steam_id
        
        if 'steamcommunity.com/id/' in steam_input:
            vanity_url = steam_input.split('/id/')[-1].split('/')[0]
        else:
            vanity_url = steam_input
        
        try:
            url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
            params = {
                'key': api_key,
                'vanityurl': vanity_url,
                'url_type': 1
            }
            
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get('response', {}).get('success') == 1:
                    resolved_id = data['response']['steamid']
                    return resolved_id
                elif data.get('response', {}).get('success') == 42:
                    raise Exception(f"Steam profile '{vanity_url}' not found. Make sure the custom URL is correct.")
                else:
                    raise Exception(f"Could not resolve Steam custom URL: {vanity_url}. Error code: {data.get('response', {}).get('success', 'unknown')}")
            else:
                raise Exception(f"Steam API returned status code: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error while resolving Steam ID '{steam_input}': {str(e)}")
        except Exception as e:
            return self.try_alternative_resolution(vanity_url, steam_input)
    
    def try_alternative_resolution(self, vanity_url, original_input):
        try:
            profile_url = f"https://steamcommunity.com/id/{vanity_url}/"
            
            headers = {
                'User-Agent': 'Missing-Mettle-TF2-Checker/1.0'
            }
            
            response = requests.get(profile_url, headers=headers, timeout=10, allow_redirects=True)
            
            if response.url and '/profiles/' in response.url:
                steam_id = response.url.split('/profiles/')[-1].split('/')[0]
                if steam_id.isdigit() and len(steam_id) == 17:
                    return steam_id
            
            if response.status_code == 200:
                raise Exception(f"Custom URL '{vanity_url}' exists but couldn't be resolved. Try using your SteamID64 instead.")
            else:
                raise Exception(f"Steam profile '{vanity_url}' not found (HTTP {response.status_code}). Please check the custom URL or use your SteamID64.")
                
        except requests.exceptions.RequestException:
            raise Exception(f"Failed to resolve '{original_input}'. Please use your SteamID64 (17-digit number starting with 7656119) instead of custom URL.")
    
    def fetch_paginated_inventory(self, steam_id: str, start_assetid: str = None) -> Dict[str, any]:
        url = f"https://steamcommunity.com/inventory/{steam_id}/440/2"
        
        params = {}
        if start_assetid:
            params['start_assetid'] = start_assetid
        
        headers = {
            'User-Agent': 'Missing-Mettle-TF2-Checker/1.0'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 403:
            raise Exception("Steam inventory is private. Please set your Steam profile to PUBLIC and try again.")
        elif response.status_code == 500:
            raise Exception("Steam servers are having issues. Please try again later.")
        elif response.status_code == 404:
            raise Exception("Steam profile not found. Please check the Steam ID/URL.")
        elif response.status_code != 200:
            raise Exception(f"Steam API returned status code: {response.status_code}")
        
        try:
            data = response.json()
            return data
        except json.JSONDecodeError as e:
            raise Exception("Invalid response from Steam. The inventory might be empty or private.")

    def is_unique_weapon(self, item_info: Dict[str, any]) -> bool:
        tags = item_info.get('tags', [])
        
        is_weapon = False
        is_unique = False
        
        for tag in tags:
            tag_name = tag.get('localized_tag_name', '').lower()
            tag_category = tag.get('category', '').lower()
            
            if (tag_category == 'type' and 'weapon' in tag_name) or \
               (tag_category == 'class' and any(weapon_type in tag_name for weapon_type in 
                ['primary', 'secondary', 'melee', 'pda', 'pda2'])):
                is_weapon = True
            
            if tag_category == 'quality' and tag_name == 'unique':
                is_unique = True
        
        return is_weapon and is_unique
    
    def fetch_steam_inventory(self, steam_input, api_key):
        try:
            steam_id = self.resolve_steam_id(steam_input, api_key)
            
            all_weapons = set()
            start_assetid = None
            page_num = 1
            total_items_processed = 0
            
            while True:
                self.status_var.set(f"Fetching inventory page {page_num}...")
                
                data = self.fetch_paginated_inventory(steam_id, start_assetid)
                
                if not data.get('success'):
                    if 'error' in data:
                        raise Exception(f"Steam API error: {data.get('error', 'Unknown error')}")
                    else:
                        raise Exception("Steam inventory could not be loaded (might be private or empty)")
                
                descriptions = {item['classid']: item for item in data.get('descriptions', [])}
                assets = data.get('assets', [])
                
                page_weapons = 0
                for item in assets:
                    class_id = item['classid']
                    if class_id in descriptions:
                        item_info = descriptions[class_id]
                        item_name = item_info.get('market_hash_name', item_info.get('name', ''))
                        
                        tags = item_info.get('tags', [])
                        is_weapon = False
                        is_problematic_item = any(prob in item_name.lower() for prob in ['cloak and dagger', 'dead ringer', 'red-tape recorder'])
                        
                        for tag in tags:
                            tag_name = tag.get('localized_tag_name', '').lower()
                            tag_category = tag.get('category', '').lower()
                            
                            if (tag_category == 'type' and 'weapon' in tag_name) or \
                               (tag_category == 'class' and any(weapon_type in tag_name for weapon_type in 
                                ['primary', 'secondary', 'melee', 'pda', 'pda2'])) or \
                               (tag_category == 'type' and any(special_type in tag_name for special_type in
                                ['watch', 'sapper', 'building', 'invis watch'])):
                                is_weapon = True
                                break
                        
                        if not is_weapon:
                            item_name_lower = item_name.lower()
                            special_items = [
                                'cloak and dagger', 'dead ringer', 'red-tape recorder', 
                                'invis watch', 'sapper', 'ap-sap', 'snack attack'
                            ]
                            if any(special in item_name_lower for special in special_items):
                                is_weapon = True
                        
                        if is_weapon and item_name:
                            all_weapons.add(item_name)
                            page_weapons += 1
                
                total_items_processed += len(assets)
                
                if data.get('more_items'):
                    if assets:
                        start_assetid = assets[-1]['assetid']
                        page_num += 1
                        time.sleep(1)
                    else:
                        break
                else:
                    break
            
            return all_weapons
            
        except Exception as e:
            raise Exception(f"Failed to fetch Steam inventory: {str(e)}")
    
    def check_weapons(self):
        if not self.api_key_var.get():
            self.show_error_dialog("Please enter your Steam API key")
            return
            
        if not self.steam_id_var.get():
            self.show_error_dialog("Please enter a Steam ID")
            return
        
        if not self.load_weapons_data():
            return
        
        thread = threading.Thread(target=self.check_weapons_thread)
        thread.daemon = True
        thread.start()
    
    def show_error_dialog(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")
        error_window.geometry("400x150")
        error_window.configure(bg=self.colors['bg_primary'])
        error_window.resizable(False, False)
        error_window.transient(self.root)
        error_window.grab_set()
        
        error_window.update_idletasks()
        x = (error_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (error_window.winfo_screenheight() // 2) - (150 // 2)
        error_window.geometry(f"400x150+{x}+{y}")
        
        msg_label = tk.Label(error_window, text=message, 
                            bg=self.colors['bg_primary'], 
                            fg=self.colors['fg_primary'],
                            font=('Segoe UI', 10),
                            wraplength=350)
        msg_label.pack(expand=True, pady=20)
        
        ok_btn = tk.Button(error_window, text="OK", 
                          bg=self.colors['bg_tertiary'], 
                          fg=self.colors['fg_primary'],
                          font=('Segoe UI', 9),
                          borderwidth=1,
                          relief='solid',
                          command=error_window.destroy)
        ok_btn.pack(pady=(0, 20))
    
    def check_weapons_thread(self):
        try:
            self.status_var.set("Fetching Steam inventory...")
            
            self.user_weapons = self.fetch_steam_inventory(
                self.steam_id_var.get(), 
                self.api_key_var.get()
            )
            
            self.status_var.set(f"Found {len(self.user_weapons)} weapons in inventory. Comparing...")
            
            self.find_missing_and_obtained_weapons()
            
            self.apply_filters()
            self.update_obtained_display()
            
            missing_count = len(self.filtered_missing_weapons)
            obtained_count = len(self.obtained_weapons)
            unlockable_total = len([w for w in self.all_weapons if w['tier'] != 'Stock'])
            
            self.status_var.set(f"Found {missing_count} missing weapons, {obtained_count} obtained weapons. Total unlockable: {unlockable_total}")
            
        except Exception as e:
            self.show_error_dialog(str(e))
            self.status_var.set("Error occurred during check")
    
    def find_missing_and_obtained_weapons(self):
        user_weapon_names = set()
        
        problematic_weapons = ['cloak and dagger', 'dead ringer', 'red-tape recorder']
        
        for weapon in self.user_weapons:
            original_name = weapon
            clean_name = weapon
            
            is_problematic = any(prob in weapon.lower() for prob in problematic_weapons)
            
            prefixes = [
                'Specialized Killstreak ', 'Professional Killstreak ', 'Killstreak ',
                'Strange Unusual ', 'Haunted ', 'Collector\'s ', 'Decorated ',
                'Strange ', 'Vintage ', 'Genuine ', 'Unusual ', 'Unique ', 'Normal ',
                'Self-Made ', 'Community ', 'Valve ', 'The '
            ]
            
            changed = True
            while changed:
                changed = False
                for prefix in prefixes:
                    if clean_name.startswith(prefix):
                        clean_name = clean_name[len(prefix):]
                        changed = True
                        break
                
            user_weapon_names.add(clean_name)
        
        self.missing_weapons = []
        self.obtained_weapons = []
        
        for weapon in self.all_weapons:
            if weapon['tier'] == 'Stock':
                continue
                
            weapon_name = weapon['name']
            
            if weapon_name in user_weapon_names:
                self.obtained_weapons.append(weapon)
            else:
                self.missing_weapons.append(weapon)
    
    def apply_filters(self, event=None):
        if not hasattr(self, 'missing_weapons'):
            return
        
        self.filtered_missing_weapons = []
        
        for weapon in self.missing_weapons:
            if not self.class_filters.get(weapon['class'], tk.BooleanVar(value=True)).get():
                continue
            
            if not self.slot_filters.get(weapon['slot'], tk.BooleanVar(value=True)).get():
                continue
            
            if not self.type_filters.get(weapon['type'], tk.BooleanVar(value=True)).get():
                continue
            
            self.filtered_missing_weapons.append(weapon)
        
        self.update_missing_display()
    
    def update_missing_display(self):
        for item in self.missing_tree.get_children():
            self.missing_tree.delete(item)
        
        for weapon in self.filtered_missing_weapons:
            class_name = self.class_names.get(weapon['class'], f"Class {weapon['class']}")
            slot_name = self.slot_names.get(weapon['slot'], f"Slot {weapon['slot']}")
            self.missing_tree.insert('', 'end', values=(
                weapon['name'],
                class_name,
                slot_name,
                weapon['tier'],
                weapon['type'],
                weapon['tag']
            ))
    
    def update_obtained_display(self):
        for item in self.obtained_tree.get_children():
            self.obtained_tree.delete(item)
        
        for weapon in self.obtained_weapons:
            class_name = self.class_names.get(weapon['class'], f"Class {weapon['class']}")
            slot_name = self.slot_names.get(weapon['slot'], f"Slot {weapon['slot']}")
            self.obtained_tree.insert('', 'end', values=(
                weapon['name'],
                class_name,
                slot_name,
                weapon['tier'],
                weapon['type'],
                weapon['tag']
            ))

def main():
    root = tk.Tk()
    app = TF2WeaponChecker(root)
    
    def show_help():
        help_window = tk.Toplevel(root)
        help_window.title("Missing Mettle - Setup Help")
        help_window.geometry("600x450")
        help_window.configure(bg=app.colors['bg_primary'])
        help_window.resizable(False, False)
        
        main_frame = tk.Frame(help_window, bg=app.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        help_text = """How to set up Missing Mettle:

1. Steam API Key:
   • Go to https://steamcommunity.com/dev/apikey
   • Register for a free Steam Web API key
   • Enter the key in the "Steam API Key" field

2. Steam ID/URL (any of these formats work):
   • SteamID64: 76561198XXXXXXXXX (17 digits)
   • Custom URL: just the username (e.g., "7eventy7")
   • Profile URL: https://steamcommunity.com/id/username
   • Profile URL: https://steamcommunity.com/profiles/76561198XXXXXXXXX
   
   IMPORTANT: The Steam profile's inventory must be set to PUBLIC!

3. Filters (only affect Missing Weapons):
   • Use checkboxes to filter missing weapons results
   • All filters are checked by default (showing all missing weapons)
   • Uncheck categories you don't want to see in missing weapons
   • Class: Filter by TF2 character class
   • Slot: Primary/Secondary/Melee/Special weapons
   • Type: Normal weapons vs Reskins

4. Weapon Panels:
   • Missing Weapons: Shows unlockable weapons you don't have (filtered)
   • Obtained Weapons: Shows unlockable weapons you do have (unfiltered)
   • Stock weapons are excluded from both panels

Note: ALL weapon qualities are counted (Strange, Vintage, Genuine, Killstreak, etc.). 
The app automatically cleans weapon names by removing quality prefixes for matching.
For example, "Strange Killstreak Natascha" is detected as "Natascha".

Troubleshooting:
   • If you get a 404 error: Check the Steam ID format and make sure the profile exists
   • If you get a 403 error: Make sure the Steam inventory is set to PUBLIC
   • If no weapons are found: The inventory might be empty or items aren't recognized as weapons
   • Make sure list.json is in the same folder as this script"""
        
        text_widget = tk.Text(main_frame, wrap=tk.WORD, padx=10, pady=10, 
                             bg=app.colors['bg_secondary'], 
                             fg=app.colors['fg_primary'], 
                             insertbackground=app.colors['fg_primary'],
                             selectbackground=app.colors['bg_selected'],
                             font=('Segoe UI', 9),
                             borderwidth=1,
                             relief='solid')
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert('1.0', help_text)
        text_widget.config(state=tk.DISABLED)
        
        close_btn = tk.Button(main_frame, text="Close", 
                             bg=app.colors['bg_tertiary'], 
                             fg=app.colors['fg_primary'],
                             font=('Segoe UI', 9),
                             borderwidth=1,
                             relief='solid',
                             command=help_window.destroy)
        close_btn.pack(pady=(10, 0))
    
    help_button = tk.Button(root, text="Help", 
                           bg=app.colors['bg_tertiary'], 
                           fg=app.colors['fg_primary'],
                           font=('Segoe UI', 9),
                           borderwidth=1,
                           relief='solid',
                           command=show_help)
    help_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()