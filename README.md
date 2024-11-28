# folder_sync 

Usage:

python script_name.py "path to source folder" "path to replica folder" "path to log file" synchronization_interval


Usage example: 
python folder_sync.py "C:\Users\pops\Desktop\folder_sync\source" "C:\Users\pops\Desktop\folder_sync\replica" "C:\Users\pops\Desktop\folder_sync\logs"  5


Make sure all paths exist, especially the source folder. The script will create the replica folder and the log file if they don’t exist.

The script will keep synchronizing every synchronization_interval seconds until you stop it (Ctrl+C on most systems).

Both the console and the log file will show messages about file creation, updates, and removals during synchronization.
