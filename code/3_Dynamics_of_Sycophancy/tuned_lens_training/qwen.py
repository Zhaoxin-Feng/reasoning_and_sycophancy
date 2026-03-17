import os
import importlib
import tuned_lens
import transformers.models.llama.modeling_llama
import transformers.models.qwen2.modeling_qwen2
import transformers.models.gemma2.modeling_gemma2 # Added Gemma 2

print("Performing surgery to force Tuned Lens support for Qwen2 and Gemma 2...")

# 1. Locate the package directory
package_dir = os.path.dirname(tuned_lens.__file__)
target_file = os.path.join(package_dir, "model_surgery.py")

# 2. Define code snippets for different states
# Original code (Llama only)
code_llama_only = "elif isinstance(base_model, models.llama.modeling_llama.LlamaModel):"

# Legacy patch code (Llama + Qwen support)
code_llama_qwen = "elif isinstance(base_model, (models.llama.modeling_llama.LlamaModel, models.qwen2.modeling_qwen2.Qwen2Model)):"

# Target code (Llama + Qwen + Gemma 2 support)
# Note: Gemma 2 structure is similar and can be handled like Llama/Qwen, ensuring transformers version is current.
new_code_all = "elif isinstance(base_model, (models.llama.modeling_llama.LlamaModel, models.qwen2.modeling_qwen2.Qwen2Model, models.gemma2.modeling_gemma2.Gemma2Model)):"

# 3. Read and modify
if os.path.exists(target_file):
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Check current status
    if "Gemma2Model" in content:
        print("✅ Code already contains Gemma 2 support, no modification needed.")
        
    elif code_llama_qwen in content:
        # Case A: Qwen patch was previously applied, now appending Gemma support
        print("ℹ️ Qwen support detected, appending Gemma 2 support...")
        content = content.replace(code_llama_qwen, new_code_all)
        modify = True
        
    elif code_llama_only in content:
        # Case B: Original library file, adding both Qwen and Gemma support
        print("ℹ️ Original library file detected, adding Qwen and Gemma 2 support...")
        content = content.replace(code_llama_only, new_code_all)
        modify = True
        
    else:
        modify = False
        print(f"⚠️ Warning: Expected code line not found in {target_file}.")
        print("The library version may have changed or the file is in an unknown state.")
        # Debugging output
        start_idx = content.find("elif isinstance(base_model,")
        if start_idx != -1:
             print("Found suspected target line:", content[start_idx:start_idx+200])

    # If modification is required, write to file
    if 'modify' in locals() and modify:
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Successfully patched {target_file}!\nTuned Lens can now recognize Qwen2 and Gemma 2.")

else:
    print(f"❌ Error: File not found {target_file}")

# 4. Reload module to ensure changes take effect
import tuned_lens.model_surgery
importlib.reload(tuned_lens.model_surgery)
print("Module reloaded.")