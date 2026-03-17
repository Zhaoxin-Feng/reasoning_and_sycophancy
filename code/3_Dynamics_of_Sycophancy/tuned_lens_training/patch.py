import os
import tuned_lens

def main():
    # 1. Automatically locate the path of the library file
    # i.e., /usr/local/lib/python3.12/dist-packages/tuned_lens/scripts/ingredients.py
    base_path = os.path.dirname(tuned_lens.__file__)
    target_file = os.path.join(base_path, "scripts", "ingredients.py")

    print(f"Locating target file: {target_file}")

    if not os.path.exists(target_file):
        print(f"❌ Error: File not found {target_file}")
        return

    # 2. Read file content
    with open(target_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 3. Define the target line signature and code to insert
    # Target: Find the line where the dataset is loaded
    target_signature = "dataset = load_dataset(*self.name, split=self.split, revision=self.revision)"

    # Patch code to insert (Note: indentation must be 8 spaces to match context)
    patch_code = [
        "\n",
        "        # === [Auto-Patch] Fix for RedPajama raw_content ===\n",
        "        if 'raw_content' in dataset.column_names:\n",
        "            print('Detected raw_content column, renaming to text...')\n",
        "            dataset = dataset.rename_column('raw_content', 'text')\n",
        "        # ==================================================\n"
    ]

    # 4. Execute replacement
    new_lines = []
    is_patched = False
    already_patched = False

    for i, line in enumerate(lines):
        new_lines.append(line)

        # If the target line is found
        if target_signature in line:
            # Check if the next line is already our patch (prevent duplicate insertion)
            if i + 2 < len(lines) and "[Auto-Patch]" in lines[i+2]:
                already_patched = True
                break

            # Insert patch
            new_lines.extend(patch_code)
            is_patched = True

    # 5. Write back to file
    if already_patched:
        print("✅ File has already been modified, no operation needed.")
    elif is_patched:
        try:
            with open(target_file, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print("✅ Success! Modified tuned-lens source code; now supports raw_content field.")
        except PermissionError:
            print("❌ Permission denied. Try using sudo (though default is often root on RunPod).")
    else:
        print("❌ Warning: Target line not found. tuned-lens version might have updated, script failed.")

if __name__ == "__main__":
    main()