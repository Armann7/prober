# Prober

**Prober** is an automated reconnaissance and vulnerability probing tool designed for bug bounty programs. It processes publicly available bounty scope definitions, discovers relevant assets, and performs automated security scanning to identify high-severity issues.

## Overview

Prober consumes structured scope data from bug bounty target repositories, filters and expands eligible assets, and executes automated scans using OWASP ZAP. The resulting reports are analyzed to extract high-priority vulnerabilities suitable for further manual validation.

## Probing Workflow

The probing process consists of the following stages:

1. **Load target definitions**

   * Parse JSON files from a cloned copy of
     [https://github.com/arkadiyt/bounty-targets-data.git](https://github.com/arkadiyt/bounty-targets-data.git)

2. **Scope filtering**

   * Retain only `in_scope` resources
   * Supported resource types include (but are not limited to):

     * `website`
     * `api`
     * `url`

3. **Asset expansion**

   * Resolve and enumerate subdomains for templated or wildcard entries

4. **Automated scanning**

   * Execute OWASP ZAP scans against each resolved resource

5. **Result analysis**

   * Parse ZAP reports
   * Extract vulnerabilities classified with **HIGH** severity

## Interface

Prober is operated via a command-line interface (CLI).

### Parameters

* `bounty-targets-data`
  Path to a file or a directory containing JSON scope files (from the cloned repository)

* `outdir`
  Path to the directory where scan results and reports will be written

## Intended Use

Prober is intended for:

* Initial reconnaissance of bug bounty scopes
* Automated identification of high-severity findings
* Assisting security researchers in prioritizing manual testing efforts

Use this tool only against assets for which you have explicit authorization.
