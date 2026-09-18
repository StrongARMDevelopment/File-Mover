# File-Mover

Automatically moves files from one location to another, based on folder creation metadata rather than a manual, all-at-once transfer.

## The Problem

At Harbor Fab, every project bid lived in a shared server folder, organized by year. By year's end, a single year's folder held hundreds of files across many gigabytes. Attempting a bulk transfer of an entire year's folder in one shot would overload the server, causing failed transfers and, at times, crashing the server outright.

## What It Does

File-Mover reads the creation metadata of every folder inside a selected target directory, then lets the user:

1. Choose the year to target (based on folder creation date)
2. Choose a destination server and folder
3. Run the move

The tool then batch-moves only the matching files automatically, in manageable batches, instead of attempting the entire transfer at once. No manual sorting, no server overload.

## Why It Matters

This replaced a fully manual, error-prone process that had previously crashed the company's server under transfer load. It now runs cleanly at year-end with no manual intervention, saving hours of work annually.

## Tech

Python, with a simple interface for selecting target year, source folder, and destination.

## Status

Built independently while working full-time in a non-technical role. Still in production use today.
