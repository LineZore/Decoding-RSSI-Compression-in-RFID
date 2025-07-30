# RSSI Correction and ITP Measurement

This project provides implementations and partial datasets for RSSI correction and in-situ Interrogation Threshold Power (ITP) measurements in RFID systems.

### Related Paper
**Title**: *Decoding RSSI Compression in RFID: Dynamic RCS Modeling and Tag-Intrinsic Power Metrics for Reliable Backscatter Networks*

## 1. demo_from_reader

This demo shows how to collect data using the Impinj R420 reader, perform RSSI correction, and measure ITP in-situ.

### Requirements

Hardware:
- Reader: `Impinj R420`
- Tag: `ALN9640`

Software:
- Ubuntu 20.04
- OpenJDK 11
- Python 3.10
- Dependencies:
  - `numpy`,
  - `matplotlib`.

---

### Directory Structure

```text
demo_from_reader/
│
├── bin/                  # Compiled Java classes
│
├── data/                 # Collected data (ref.txt, ver.txt)
│
├── lib/                  # Impinj R420 SDK
│   └──OctaneSDKJava-4.0.0.0-jar-with-dependencies.jar      
│
├── python/               # Python scripts for processing
│   ├── ITP_measure.py
│   └── RSSI_correct.py
│
├── src/                  # Java source code
│   └── reader/
│       ├──ReadRSSIByPower.java                   # Code for collecting data
│       └──TagReportListenerImplementation.java   # Callback function
│
└── README.md
```

---

### Running the Demonstrations

**Step 1: Compile Java Code**

Navigate to `demo_from_reader/` and run:


```bash
javac -cp "lib/*" -d bin/ src/reader/*
```

This compiles the Java files into the `bin/reader/` directory.

---

**Step 2: Collect RSSI Data**

Use the following command to collect **reference RSSI** data:

```bash
java -cp "bin/:lib/*" reader.ReadRSSIByPower <READER_NAME> <TAG_EPC> "ref"
```

Replace:
- `<READER_NAME>` with your reader's hostname (e.g., `speedwayr-15-0A-55.local`)
- `<TAG_EPC>` with your tag’s EPC (e.g., `E28068940000403020250728`)

This creates `ref.txt` in the `data/` folder.

To collect **verification RSSI** data:

```bash
java -cp "bin/:lib/*" reader.ReadRSSIByPower <READER_NAME> <TAG_EPC> "ver"
```

This creates `ver.txt` in `data/`.

> ⚠️ **Note**: Both datasets must be collected *under the presence of ITP*. If tags are readable at the minimum power (10 dBm), ITP cannot be determined even with power sweep.

> 💡 In real-world use, only a single RSSI and TX power pair is required for in-situ ITP measurement. Power sweeping is used here for demonstration and validation.

---

**Step 3: Analyze Results**

Run RSSI correction:

```bash
python ./python/RSSI_correct.py
```

Run ITP measurement:

```bash
python ./python/ITP_measure.py
```

---


## 2. demo_from_dataset

This demo uses a partial dataset to illustrate **RSSI correction** and **ITP measurement** without a reader.

### Requirements
- Ubuntu 20.04
- Python 3.10
- Dependencies:
  - `numpy`,
  - `matplotlib`.

---

### Directory Structure

```text
demo_from_dataset/
│
├── src/                  # Source code
│   ├── ITP_measure.py
│   └── RSSI_correct.py
│
├── data/                 # Input data
│   ├── 9640.txt          
│   ├── R6P.txt
│   └── U8.txt
│
└── README.md
```

---

### Running the Demonstrations

Ensure that it is in the `demo_from_dataset/` directory.

Run the following to view the RSSI correction results:

```bash
python ./src/RSSI_correct.py
```

Run the following to view the ITP measurement results:

```bash
python ./src/ITP_measure.py
```

---

### Dataset Description

Each `.txt` file (e.g., `9640.txt`, `R6P.txt`, `U8.txt`) contains RSSI readings for a tag:

- **7 segments**: Each represents a different tag-reader distance (from **2 m to 8 m**).
- **5 lines per segment**: Each line is one independent RFID tag.
- **91 RSSI values per line**: 
  - Correspond to TX powers from **10 dBm to 32.5 dBm**
  - Power step: **0.25 dBm**

