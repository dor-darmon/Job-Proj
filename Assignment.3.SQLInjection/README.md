# Assignment 3: SQL Injection Simulation

## Overview
This is a C# Desktop Application designed to demonstrate a SQL Injection attack and its mitigation.
It fulfills the assignment requirements by providing a UI with two modes:
1. Vulnerable Login (String Concatenation)
2. Secure Login (Parameterized Logic)

## Prerequisites
* Windows OS
* .NET Framework (Pre-installed on almost all Windows PCs)
* No Visual Studio installation required to run.

## How to Compile and Run
1. Save the code file as "SQLInjectionApp.cs".
2. Open the Command Prompt (cmd.exe).
3. Navigate to the folder where you saved the file.
4. Run the following command to compile (this uses the built-in C# compiler):

   C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe SQLInjectionApp.cs

5. A new file named "SQLInjectionApp.exe" will appear in the folder.
6. Double-click "SQLInjectionApp.exe" to run the application.

## Usage Guide

### Scenario 1: The Attack
1. Go to the "Vulnerable Login" tab.
2. In the Username field, type: ' OR '1'='1
3. Leave password empty or type anything.
4. Click Login.
5. Observation: Login succeeds. The Log area shows the manipulated query.

### Scenario 2: The Mitigation
1. Go to the "Secure Login" tab.
2. In the Username field, type: ' OR '1'='1
3. Click Login.
4. Observation: Login fails. The Log area shows that the input was treated as a literal string, not as code.