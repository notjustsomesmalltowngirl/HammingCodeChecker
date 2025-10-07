# 🧮 Hamming Code Checker

A Python utility for **detecting and correcting single-bit errors** in binary codewords using the **Hamming error-correcting code algorithm**.  
This tool provides a reliable and efficient way to verify data integrity in digital communication and storage systems.

---

## ✨ Features

- ✅ **Error Detection** – Quickly identifies whether a transmitted or stored codeword contains a single-bit error.  
- 🛠 **Error Correction** – Locates the erroneous bit and automatically corrects it, restoring the original, error-free data.  
- 💾 **Data Recovery** – Extracts the original data bits from a valid or corrected codeword.  
- ⚙ **Flexible** – Supports different Hamming code variations and bit lengths.

---

## 🧠 How It Works

Hamming codes insert **parity bits** at positions that are powers of two (1, 2, 4, 8, …).  
The Hamming Code Checker uses these parity bits to detect and fix single-bit errors:

1. **🔍 Parity Check**  
   Performs a series of parity checks on relevant groups of bits within the codeword.  

2. **🧮 Syndrome Calculation**  
   For each failed parity check, its bit position is noted.  
   The binary sum of these positions forms the **syndrome**, which pinpoints the exact location of the error.  

3. **♻ Correction**  
   The bit at the error location is flipped to repair the codeword.  

4. **📤 Data Extraction**  
   After validation or correction, the original data bits are extracted by removing the parity bits.


## 🧠 About The Hamming Code

**Hamming Code** is a classic error-detecting and error-correcting code invented by **Richard W. Hamming** in 1950 and taught at the [University of Lagos](https://unilag.edu.ng/)
under the course titled *Introduction to discrete and data structures* (CSC224).  
It’s designed to detect and correct **single-bit errors** in transmitted or stored binary data by adding extra **parity bits** at strategic positions within the codeword.

### 📌 Key Ideas
- Parity bits are placed at positions that are **powers of two** (1, 2, 4, 8, …).  
- Each parity bit checks a specific set of data bits according to its binary position.  
- If an error occurs during transmission, the parity checks will “fail” in a pattern that identifies the **exact bit position** of the error.  
- Flipping that bit restores the original, correct codeword.

---

## 🚀 Usage

```bash
# Clone the repository
git clone https://github.com/notjustsomesmalltowngirl/HammingCodeChecker.git
cd HammingCodeChecker

