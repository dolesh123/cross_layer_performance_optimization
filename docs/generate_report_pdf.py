import os
import subprocess

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Major Project Report - IMPOF</title>
<style>
  @page {
    size: A4 portrait;
    margin: 20mm 20mm 20mm 25mm;
    @bottom-center {
      content: counter(page);
    }
  }
  
  body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    line-height: 1.6;
    color: #111111;
    margin: 0;
    padding: 0;
    background: #ffffff;
  }

  .page {
    width: 100%;
    min-height: 1050px;
    box-sizing: border-box;
    padding: 20px 0;
    page-break-after: always;
    position: relative;
  }

  .page-border {
    border: 1.5px solid #222222;
    padding: 35px 40px;
    min-height: 980px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .page-border-normal {
    border: 1.5px solid #222222;
    padding: 35px 40px;
    min-height: 980px;
    box-sizing: border-box;
  }

  .text-center { text-align: center; }
  .text-justify { text-align: justify; text-justify: inter-word; }
  .text-right { text-align: right; }
  .bold { font-weight: bold; }
  .uppercase { text-transform: uppercase; }

  h1.report-main-title {
    font-size: 16pt;
    font-weight: bold;
    line-height: 1.4;
    margin: 15px 0;
    text-align: center;
  }

  h2.chapter-title {
    font-size: 15pt;
    font-weight: bold;
    text-align: center;
    margin-top: 25px;
    margin-bottom: 25px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }

  h3.section-title {
    font-size: 13pt;
    font-weight: bold;
    margin-top: 18px;
    margin-bottom: 10px;
    text-transform: uppercase;
  }

  h4.subsection-title {
    font-size: 12pt;
    font-weight: bold;
    margin-top: 14px;
    margin-bottom: 6px;
  }

  p {
    margin-top: 6px;
    margin-bottom: 12px;
    text-align: justify;
    text-indent: 0;
  }

  .page-num {
    text-align: center;
    font-size: 11pt;
    font-weight: bold;
    margin-top: 20px;
  }

  .page-num-top {
    text-align: center;
    font-size: 11pt;
    font-weight: bold;
    margin-bottom: 15px;
  }

  table.formal-table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 10.5pt;
  }

  table.formal-table th, table.formal-table td {
    border: 1px solid #333333;
    padding: 7px 10px;
    text-align: left;
  }

  table.formal-table th {
    background-color: #f2f2f2;
    font-weight: bold;
    text-align: center;
  }

  table.toc-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 11pt;
    margin-top: 15px;
  }

  table.toc-table td {
    padding: 4px 0;
    vertical-align: bottom;
  }

  table.toc-table tr td:first-child {
    width: 15%;
    font-weight: bold;
  }

  table.toc-table tr td:nth-child(2) {
    width: 75%;
  }

  table.toc-table tr td:last-child {
    width: 10%;
    text-align: right;
    font-weight: bold;
  }

  .college-logo-placeholder {
    width: 100px;
    height: 100px;
    margin: 15px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid #006633;
    border-radius: 50%;
    color: #006633;
    font-weight: bold;
    font-size: 12pt;
    text-align: center;
    padding: 5px;
    box-sizing: border-box;
  }

  .signature-table {
    width: 100%;
    margin-top: 35px;
    border: none;
  }

  .signature-table td {
    border: none;
    vertical-align: top;
    padding: 0;
  }

  .sign-line {
    border-bottom: 1px solid #111;
    width: 180px;
    display: inline-block;
    margin-top: 35px;
  }

  .diagram-container {
    border: 1px solid #ccc;
    background: #fafafa;
    padding: 15px;
    margin: 15px 0;
    border-radius: 4px;
    text-align: center;
  }

  .formula-box {
    background: #f7f9fa;
    border-left: 3px solid #333;
    padding: 10px 15px;
    margin: 12px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size: 11pt;
  }

  ul, ol {
    margin-top: 5px;
    margin-bottom: 12px;
    padding-left: 25px;
  }

  li {
    margin-bottom: 5px;
    text-align: justify;
  }

  @media print {
    body { background: white; }
    .page { page-break-after: always; min-height: auto; padding: 0; }
  }
</style>
</head>
<body>

<!-- PAGE 1: TITLE PAGE -->
<div class="page">
  <div class="page-border">
    <div class="text-center">
      <p style="font-size: 13pt; font-weight: bold; margin-bottom: 5px;">A MAJOR PROJECT REPORT ON</p>
      <h1 class="report-main-title">
        INTEGRATED MULTI-LAYER PERFORMANCE OPTIMIZATION FRAMEWORK FOR WEB APPLICATIONS (IMPOF)
      </h1>
      <p style="font-size: 11pt; margin-top: 15px;">Submitted by,</p>
      <table style="margin: 0 auto; width: 65%; font-size: 11pt; font-weight: bold; text-align: left;">
        <tr><td>N. DEEKSHITH KUMAR</td><td style="text-align: right;">23J41A3345</td></tr>
        <tr><td>P. RAVINDAR NAYAK</td><td style="text-align: right;">23J41A3348</td></tr>
        <tr><td>P. DOLESHWAR</td><td style="text-align: right;">24J45A3305</td></tr>
        <tr><td>J. GURUNATH</td><td style="text-align: right;">23J41A3328</td></tr>
        <tr><td>M. AAKASH</td><td style="text-align: right;">23J41A3301</td></tr>
      </table>
    </div>

    <div class="text-center" style="margin: 20px 0;">
      <p style="font-style: italic; font-size: 11.5pt; margin: 4px 0;">In partial fulfillment of the requirements for the award of the degree of</p>
      <p style="font-size: 13pt; font-weight: bold; margin: 4px 0;">BACHELOR OF TECHNOLOGY</p>
      <p style="font-size: 11.5pt; margin: 4px 0;">In</p>
      <p style="font-size: 12pt; font-weight: bold; margin: 4px 0;">COMPUTER SCIENCE AND INFORMATION TECHNOLOGY</p>
      
      <p style="font-size: 11pt; margin-top: 15px; margin-bottom: 2px;">Under the Guidance of</p>
      <p style="font-size: 12pt; font-weight: bold; margin: 2px 0;">Mr. M. RAVINDRA BABU</p>
      <p style="font-size: 11pt; margin: 2px 0;">Assistant Professor, Information Technology</p>
    </div>

    <div class="text-center">
      <div class="college-logo-placeholder">
        <span>MREC<br><small style="font-size: 8pt;">ESTD 2002</small></span>
      </div>
      <p style="font-size: 12pt; font-weight: bold; margin: 3px 0;">COMPUTER SCIENCE AND INFORMATION TECHNOLOGY</p>
      <p style="font-size: 14pt; font-weight: bold; margin: 3px 0;">MALLA REDDY ENGINEERING COLLEGE</p>
      <p style="font-size: 10pt; margin: 2px 0;">(An UGC Autonomous Institution, Approved by AICTE, New Delhi & Affiliated to JNTUH, Hyderabad)</p>
      <p style="font-size: 10.5pt; margin: 2px 0;">Maisammaguda, Secunderabad, Telangana, India 500100</p>
      <p style="font-size: 12pt; font-weight: bold; margin-top: 12px;">MAY-2026</p>
    </div>
  </div>
</div>

<!-- PAGE 2: BONAFIDE CERTIFICATE -->
<div class="page">
  <div class="page-border-normal">
    <div class="text-center">
      <p style="font-size: 14pt; font-weight: bold; margin: 0;">MALLA REDDY ENGINEERING COLLEGE</p>
      <p style="font-size: 10.5pt; margin: 3px 0;">Maisammaguda, Secunderabad, Telangana, India 500100</p>
      <div class="college-logo-placeholder" style="width: 75px; height: 75px; margin: 10px auto; font-size: 9pt;">
        MREC(A)
      </div>
      <h2 style="font-size: 14pt; font-weight: bold; text-decoration: underline; margin: 15px 0;">BONAFIDE CERTIFICATE</h2>
    </div>

    <p style="line-height: 1.8; margin-top: 25px;" class="text-justify">
      This is to certify that this major project work entitled <strong>“INTEGRATED MULTI-LAYER PERFORMANCE OPTIMIZATION FRAMEWORK FOR WEB APPLICATIONS (IMPOF)”</strong>, submitted by <strong>N. DEEKSHITH KUMAR (23J41A3345), P. RAVINDAR NAYAK (23J41A3348), P. DOLESHWAR (24J45A3305), J. GURUNATH (23J41A3328), M. AAKASH (23J41A3301)</strong>, Malla Reddy Engineering College affiliated to JNTUH, Hyderabad in partial fulfillment for the award of <strong>Bachelor of Technology in COMPUTER SCIENCE AND INFORMATION TECHNOLOGY</strong> is a bonafide record of project work carried out under our supervision during the academic year 2025 – 2026 and that this work has not been submitted elsewhere for a degree.
    </p>

    <table class="signature-table" style="margin-top: 60px;">
      <tr>
        <td style="width: 50%;">
          <strong>SIGNATURE</strong><br><br><br>
          <strong>Mr. M. RAVINDRA BABU</strong><br>
          Assistant Professor,<br>
          Information Technology<br>
          Malla Reddy Engineering College<br>
          Secunderabad, 500 100
        </td>
        <td style="width: 50%; text-align: right;">
          <strong>SIGNATURE</strong><br><br><br>
          <strong>Dr. DEENABABU MANDRU</strong><br>
          Professor & HOD,<br>
          Information Technology<br>
          Malla Reddy Engineering College<br>
          Secunderabad, 500 100
        </td>
      </tr>
    </table>

    <div style="margin-top: 70px;">
      <p>Submitted for Major Project viva-voce examination held on ____________________</p>
      <table style="width: 100%; margin-top: 50px; border: none;">
        <tr>
          <td style="border: none; font-weight: bold;">INTERNAL EXAMINER</td>
          <td style="border: none; font-weight: bold; text-align: right;">EXTERNAL EXAMINER</td>
        </tr>
      </table>
    </div>

    <div class="page-num">i</div>
  </div>
</div>

<!-- PAGE 3: DECLARATION -->
<div class="page">
  <div class="page-border-normal">
    <div class="text-center">
      <p style="font-size: 14pt; font-weight: bold; margin: 0;">MALLA REDDY ENGINEERING COLLEGE</p>
      <p style="font-size: 10.5pt; margin: 3px 0;">Maisammaguda, Secunderabad, Telangana, India 500100</p>
      <div class="college-logo-placeholder" style="width: 75px; height: 75px; margin: 10px auto; font-size: 9pt;">
        MREC(A)
      </div>
      <h2 style="font-size: 14pt; font-weight: bold; text-decoration: underline; margin: 15px 0;">DECLARATION</h2>
    </div>

    <p style="line-height: 1.8; margin-top: 25px;" class="text-justify">
      I hereby declare that the project titled <strong>“INTEGRATED MULTI-LAYER PERFORMANCE OPTIMIZATION FRAMEWORK FOR WEB APPLICATIONS (IMPOF)”</strong>, submitted to Malla Reddy Engineering College (Autonomous) and affiliated with JNTUH, Hyderabad, in partial fulfillment of the requirements for the award of a <strong>Bachelor of Technology in COMPUTER SCIENCE AND INFORMATION TECHNOLOGY</strong>, represents my ideas in my own words. Wherever other's ideas or words have been included, I have adequately cited and referenced the original sources. I also declare that I have adhered to all principles of academic honesty and integrity, and I have not misrepresented, fabricated, or falsified any idea, data, fact, or source in my submission. I understand that any violation of the above will become grounds for disciplinary action by the Institute. It is further declared that the project report or any part thereof has not been previously submitted to any University or Institute for the award of degree.
    </p>

    <div style="margin-top: 40px;">
      <p style="text-align: right; font-weight: bold; margin-bottom: 25px;">Signature(s)</p>
      <table style="width: 100%; border: none;">
        <tr><td style="border: none; width: 45%;">N. DEEKSHITH KUMAR</td><td style="border: none; width: 25%;">23J41A3345</td><td style="border: none; text-align: right;"><span class="sign-line"></span></td></tr>
        <tr><td style="border: none;">P. RAVINDAR NAYAK</td><td style="border: none;">23J41A3348</td><td style="border: none; text-align: right;"><span class="sign-line"></span></td></tr>
        <tr><td style="border: none;">P. DOLESHWAR</td><td style="border: none;">24J45A3305</td><td style="border: none; text-align: right;"><span class="sign-line"></span></td></tr>
        <tr><td style="border: none;">J. GURUNATH</td><td style="border: none;">23J41A3328</td><td style="border: none; text-align: right;"><span class="sign-line"></span></td></tr>
        <tr><td style="border: none;">M. AAKASH</td><td style="border: none;">23J41A3301</td><td style="border: none; text-align: right;"><span class="sign-line"></span></td></tr>
      </table>
    </div>

    <div style="margin-top: 50px;">
      <p>Secunderabad-500100</p>
      <p>Date: </p>
    </div>

    <div class="page-num">ii</div>
  </div>
</div>

<!-- PAGE 4: ACKNOWLEDGEMENT -->
<div class="page">
  <div class="page-border-normal">
    <div class="text-center">
      <p style="font-size: 14pt; font-weight: bold; margin: 0;">MALLA REDDY ENGINEERING COLLEGE</p>
      <p style="font-size: 10.5pt; margin: 3px 0;">Maisammaguda, Secunderabad, Telangana, India 500100</p>
      <h2 style="font-size: 14pt; font-weight: bold; text-decoration: underline; margin: 25px 0;">ACKNOWLEDGEMENT</h2>
    </div>

    <p style="line-height: 1.8; margin-top: 25px;" class="text-justify">
      We would like to express our sincere thanks to <strong>Dr. P. RAVINDER REDDY</strong>, Professor, Principal, MREC(A) for providing the working facilities in the college.
    </p>

    <p style="line-height: 1.8;" class="text-justify">
      Our sincere thanks and gratitude to <strong>Dr. DEENABABU MANDRU</strong>, Professor & Head, Department of <strong>COMPUTER SCIENCE AND INFORMATION TECHNOLOGY</strong> MREC(A) for all the timely support and valuable suggestions during the period of our project.
    </p>

    <p style="line-height: 1.8;" class="text-justify">
      We are thankful to our Project Coordinator <strong>Ms. M. Anusha</strong>, Assistant Professor, Department of Computer Science and Information Technology, for her cooperation during the project work.
    </p>

    <p style="line-height: 1.8;" class="text-justify">
      We are greatly thankful and indebted to our internal guide, <strong>Mr. M. RAVINDRA BABU</strong>, Assistant Professor, Department of IT, MREC(A) for his constant guidance, encouragement, and moral support throughout the project.
    </p>

    <p style="line-height: 1.8;" class="text-justify">
      Finally, we would also like to thank all the faculty and staff of the IT Department who helped us directly or indirectly, parents, and friends for their cooperation in completing the project work.
    </p>

    <div style="margin-top: 60px; float: right; width: 60%;">
      <table style="width: 100%; border: none; font-size: 11pt;">
        <tr><td style="border: none;">N. DEEKSHITH KUMAR</td><td style="border: none; text-align: right;">23J41A3345</td></tr>
        <tr><td style="border: none;">P. RAVINDAR NAYAK</td><td style="border: none; text-align: right;">23J41A3348</td></tr>
        <tr><td style="border: none;">P. DOLESHWAR</td><td style="border: none; text-align: right;">24J45A3305</td></tr>
        <tr><td style="border: none;">J. GURUNATH</td><td style="border: none; text-align: right;">23J41A3328</td></tr>
        <tr><td style="border: none;">M. AAKASH</td><td style="border: none; text-align: right;">23J41A3301</td></tr>
      </table>
    </div>

    <div style="clear: both;"></div>
    <div class="page-num">iii</div>
  </div>
</div>

<!-- PAGE 5: ABSTRACT -->
<div class="page">
  <div class="page-border-normal">
    <div class="text-center">
      <h2 style="font-size: 14pt; font-weight: bold; text-decoration: underline; margin-top: 15px; margin-bottom: 20px;">ABSTRACT</h2>
    </div>

    <p class="text-justify">
      Modern high-throughput web applications frequently suffer from severe latency degradation and throughput bottlenecks because traditional performance optimization and application monitoring paradigms operate within isolated architectural silos. Frontend developers focus exclusively on bundle sizes and client-side rendering, backend engineers profile endpoint route handlers, while database administrators examine query execution plans independently. Consequently, localized micro-optimizations fail to deliver true end-to-end performance gains when upstream thread pools block or downstream unindexed relational table scans saturate I/O channels.
    </p>

    <p class="text-justify">
      This major project presents the <strong>Integrated Multi-Layer Performance Optimization Framework (IMPOF)</strong>, an enterprise-grade observability, heuristic root-cause diagnosis, machine learning anomaly detection, and controlled performance engineering platform. IMPOF decomposes total system response time into five discrete architectural tiers: (1) Client-side Frontend Rendering, (2) Network & Transport, (3) Backend API Execution, (4) Relational Database Storage, and (5) Distributed In-Memory Cache. The framework continuously ingests telemetry spans using high-resolution nanosecond timers, evaluates health using an explainable 0–100 heuristic scoring matrix, detects multidimensional latency anomalies via an unsupervised <em>Scikit-Learn Isolation Forest</em> model, and validates systemic optimizations through controlled Before-vs-After benchmark experiments.
    </p>

    <p class="text-justify">
      The platform integrates a high-performance <strong>Node.js / Express</strong> metric ingestion backend, a <strong>Python FastAPI</strong> analytical intelligence microservice, a <strong>PostgreSQL 16</strong> relational audit store, a <strong>Redis 7.2</strong> distributed cache, and an interactive <strong>React 18</strong> DevOps command center. Empirical evaluation across a simulated production workload of 100,000+ relational entities reveals that synchronizing optimizations across all layers yields a <strong>96.1% reduction in total end-to-end response time</strong> (from 181.8 ms to 7.0 ms), cuts database query latency by <strong>99.9%</strong>, shrinks network payloads by <strong>97.3%</strong>, and scales sustained throughput by <strong>23.0x</strong> (from 24.2 RPS to 555.6 RPS) under high concurrency.
    </p>

    <div style="margin-top: 30px;">
      <p class="bold" style="margin-bottom: 6px;">KEY WORDS:</p>
      <ul>
        <li>Cross-Layer Performance Optimization</li>
        <li>Application Performance Monitoring (APM)</li>
        <li>Full-Stack Latency Decomposition</li>
        <li>Machine Learning Anomaly Detection</li>
        <li>Isolation Forest Algorithm</li>
        <li>Heuristic Bottleneck Classification</li>
        <li>Optimization Gain Index (OGI)</li>
        <li>Distributed Tracing & Web Telemetry</li>
      </ul>
    </div>

    <div class="page-num">iv</div>
  </div>
</div>

<!-- PAGE 6: TABLE OF CONTENTS (Part 1) -->
<div class="page">
  <div class="page-border-normal">
    <div class="text-center">
      <h2 style="font-size: 14pt; font-weight: bold; margin-top: 15px; margin-bottom: 25px;">TABLE OF CONTENTS</h2>
    </div>

    <table class="toc-table">
      <tr>
        <td colspan="2" style="font-weight: bold;">CERTIFICATE</td>
        <td>i</td>
      </tr>
      <tr>
        <td colspan="2" style="font-weight: bold;">DECLARATION</td>
        <td>ii</td>
      </tr>
      <tr>
        <td colspan="2" style="font-weight: bold;">ACKNOWLEDGEMENT</td>
        <td>iii</td>
      </tr>
      <tr>
        <td colspan="2" style="font-weight: bold;">ABSTRACT</td>
        <td>iv</td>
      </tr>
      <tr>
        <td colspan="2" style="font-weight: bold;">TABLE OF CONTENTS</td>
        <td>v</td>
      </tr>
    </table>

    <div style="margin-top: 30px;">
      <table class="toc-table">
        <tr style="border-bottom: 1.5px solid #000;">
          <th style="text-align: left; width: 18%;">CHAPTER</th>
          <th style="text-align: left; width: 70%;">DESCRIPTION</th>
          <th style="text-align: right; width: 12%;">PAGE NO.</th>
        </tr>
        <tr><td><strong>1</strong></td><td><strong>INTRODUCTION</strong></td><td><strong>1</strong></td></tr>
        <tr><td>1.1</td><td>INTRODUCTION & RESEARCH CONTEXT</td><td>1</td></tr>
        <tr><td><strong>2</strong></td><td><strong>LITERATURE SURVEY</strong></td><td><strong>3</strong></td></tr>
        <tr><td>2.1</td><td>LITERATURE SURVEY & RELATED WORK</td><td>3</td></tr>
        <tr><td><strong>3</strong></td><td><strong>EXISTING SYSTEM</strong></td><td><strong>4</strong></td></tr>
        <tr><td>3.1</td><td>EXISTING SYSTEM OVERVIEW</td><td>4</td></tr>
        <tr><td>3.2</td><td>DISADVANTAGES OF EXISTING SYSTEMS</td><td>5</td></tr>
        <tr><td>3.3</td><td>PROPOSED SYSTEM (IMPOF)</td><td>6</td></tr>
        <tr><td>3.4</td><td>ADVANTAGES OF PROPOSED SYSTEM</td><td>6</td></tr>
        <tr><td><strong>4</strong></td><td><strong>SYSTEM REQUIREMENTS</strong></td><td><strong>7</strong></td></tr>
        <tr><td>4.1</td><td>SYSTEM REQUIREMENTS</td><td>7</td></tr>
        <tr><td>4.1.1</td><td>H/W SYSTEM CONFIGURATION</td><td>7</td></tr>
        <tr><td>4.2</td><td>SOFTWARE REQUIREMENTS</td><td>7</td></tr>
        <tr><td><strong>5</strong></td><td><strong>SYSTEM ARCHITECTURE</strong></td><td><strong>8</strong></td></tr>
        <tr><td>5.1</td><td>SYSTEM ARCHITECTURE SPECIFICATION</td><td>8</td></tr>
      </table>
    </div>

    <div class="page-num">v</div>
  </div>
</div>

<!-- PAGE 7: TABLE OF CONTENTS (Part 2) -->
<div class="page">
  <div class="page-border-normal">
    <table class="toc-table">
      <tr style="border-bottom: 1.5px solid #000;">
        <th style="text-align: left; width: 18%;">CHAPTER</th>
        <th style="text-align: left; width: 70%;">DESCRIPTION</th>
        <th style="text-align: right; width: 12%;">PAGE NO.</th>
      </tr>
      <tr><td><strong>6</strong></td><td><strong>SYSTEM STUDY</strong></td><td><strong>9</strong></td></tr>
      <tr><td>6.1</td><td>SYSTEM STUDY</td><td>9</td></tr>
      <tr><td>6.1.1</td><td>FEASIBILITY STUDY</td><td>10</td></tr>
      <tr><td>6.1.1.a</td><td>ECONOMICAL FEASIBILITY</td><td>10</td></tr>
      <tr><td>6.1.1.b</td><td>TECHNICAL FEASIBILITY</td><td>10</td></tr>
      <tr><td>6.1.1.c</td><td>OPERATIONAL FEASIBILITY</td><td>10</td></tr>
      <tr><td><strong>7</strong></td><td><strong>SYSTEM DESIGN</strong></td><td><strong>11</strong></td></tr>
      <tr><td>7.1</td><td>SYSTEM DESIGN PRINCIPLES</td><td>11</td></tr>
      <tr><td>7.1.1</td><td>UML DIAGRAMS OVERVIEW</td><td>12</td></tr>
      <tr><td>7.1.2</td><td>CLASS DIAGRAM</td><td>13</td></tr>
      <tr><td>7.1.3</td><td>SEQUENCE DIAGRAM</td><td>14</td></tr>
      <tr><td>7.1.4</td><td>ACTIVITY DIAGRAM</td><td>15</td></tr>
      <tr><td>7.1.5</td><td>DATA FLOW DIAGRAM (DFD LEVEL 0, 1, 2)</td><td>16</td></tr>
      <tr><td>7.1.6</td><td>COMPONENT DIAGRAM</td><td>17</td></tr>
      <tr><td>7.1.7</td><td>USE CASE DIAGRAM</td><td>18</td></tr>
      <tr><td>7.1.8</td><td>DEPLOYMENT DIAGRAM</td><td>19</td></tr>
      <tr><td>7.1.9</td><td>ARCHITECTURE BLOCK DIAGRAM</td><td>20</td></tr>
      <tr><td>7.2</td><td>SOFTWARE ENVIRONMENT</td><td>21</td></tr>
      <tr><td>7.3</td><td>HISTORY AND EVOLUTION OF CORE TECHNOLOGIES</td><td>22</td></tr>
      <tr><td>7.4</td><td>MODULE DESCRIPTION</td><td>23</td></tr>
      <tr><td><strong>8</strong></td><td><strong>IMPLEMENTATION AND METHODOLOGY</strong></td><td><strong>24</strong></td></tr>
      <tr><td>8.1</td><td>IMPLEMENTATION METHODOLOGY</td><td>24</td></tr>
      <tr><td>8.2</td><td>MODULE DESCRIPTION & FUNCTIONAL SUBSYSTEMS</td><td>24</td></tr>
    </table>

    <div class="page-num">vi</div>
  </div>
</div>

<!-- PAGE 8: TABLE OF CONTENTS (Part 3) -->
<div class="page">
  <div class="page-border-normal">
    <table class="toc-table">
      <tr style="border-bottom: 1.5px solid #000;">
        <th style="text-align: left; width: 18%;">CHAPTER</th>
        <th style="text-align: left; width: 70%;">DESCRIPTION</th>
        <th style="text-align: right; width: 12%;">PAGE NO.</th>
      </tr>
      <tr><td>8.3</td><td>ALGORITHMIC IMPLEMENTATION & FORMULATION</td><td>26</td></tr>
      <tr><td>8.4</td><td>SYSTEM EXECUTION FLOW</td><td>27</td></tr>
      <tr><td><strong>9</strong></td><td><strong>SYSTEM TEST</strong></td><td><strong>28</strong></td></tr>
      <tr><td>9.1</td><td>SYSTEM TEST OVERVIEW</td><td>28</td></tr>
      <tr><td>9.2</td><td>TYPES OF TESTS (UNIT, INTEGRATION, FUNCTIONAL, STRESS)</td><td>29</td></tr>
      <tr><td>9.3</td><td>TEST CASES AND VALIDATION MATRIX</td><td>30</td></tr>
      <tr><td><strong>10</strong></td><td><strong>RESULTS AND DISCUSSIONS</strong></td><td><strong>31</strong></td></tr>
      <tr><td>10.1</td><td>FINAL OUTPUT AND INTERACTIVE SCREENSHOTS</td><td>31</td></tr>
      <tr><td>10.2</td><td>PERFORMANCE METRICS & DECOMPOSITION</td><td>33</td></tr>
      <tr><td>10.3</td><td>COMPARATIVE ANALYSIS OF OPTIMIZATION TIERS</td><td>34</td></tr>
      <tr><td>10.4</td><td>DISCUSSION OF RESULTS & OGI ANALYSIS</td><td>35</td></tr>
      <tr><td>10.5</td><td>LIMITATIONS OF CURRENT SYSTEM</td><td>36</td></tr>
      <tr><td><strong>11</strong></td><td><strong>CONCLUSION AND FUTURE SCOPE</strong></td><td><strong>37</strong></td></tr>
      <tr><td>11.1</td><td>CONCLUSION</td><td>37</td></tr>
      <tr><td>11.2</td><td>FUTURE SCOPE</td><td>38</td></tr>
      <tr><td><strong>12</strong></td><td><strong>REFERENCES / BIBLIOGRAPHY</strong></td><td><strong>39</strong></td></tr>
    </table>

    <div class="page-num">vii</div>
  </div>
</div>

<!-- PAGE 9: CHAPTER 1 - INTRODUCTION -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">1</div>
    <h2 class="chapter-title">CHAPTER-1</h2>
    <h3 class="section-title">1.1 INTRODUCTION</h3>
    
    <p class="text-justify">
      In contemporary cloud computing and distributed systems engineering, web applications have evolved into multi-layered architectures comprising client-side single page applications (SPAs), edge content delivery networks (CDNs), API gateways, asynchronous microservice backends, distributed in-memory caching tiers, and relational or NoSQL persistent databases. Delivering sub-second response times and sustaining high throughput across millions of concurrent users has become a critical requirement for enterprise software, e-commerce platforms, and mission-critical SaaS infrastructures.
    </p>

    <p class="text-justify">
      However, engineering teams routinely encounter the phenomenon of <em>architectural impedance mismatch</em> and <em>siloed optimization</em>. In conventional organizations, performance optimization is conducted in isolation: frontend developers optimize bundle sizes, implement code splitting, and monitor Google Core Web Vitals (such as Largest Contentful Paint [LCP] and Interaction to Next Paint [INP]); backend developers tune thread pool concurrency and serialize data transfer objects (DTOs); and database administrators configure B-tree indices and connection pool sizing. Despite substantial localized efforts, the overall end-to-end user latency frequently fails to improve. A hyper-optimized React frontend cannot compensate for a 700 ms unindexed table scan in the database layer, nor can an indexed database eliminate thread blocking or uncompressed 150 KB JSON payloads traversing the transport layer.
    </p>

    <p class="text-justify">
      To bridge this systemic chasm, this project develops the <strong>Integrated Multi-Layer Performance Optimization Framework (IMPOF)</strong>. IMPOF is an end-to-end, cross-layer performance observability, bottleneck classification, machine learning anomaly detection, and controlled experimentation platform. Rather than treating each tier as an opaque black box, IMPOF coordinates telemetry across five fundamental architectural layers: (1) Frontend Client Rendering, (2) Network & Transport, (3) Backend Application Runtime, (4) Persistent Database, and (5) In-Memory Cache.
    </p>

    <p class="text-justify">
      By utilizing non-invasive distributed tracing headers, high-resolution nanosecond timing hooks, an explainable 0–100 heuristic bottleneck scorer, and an unsupervised <em>Scikit-Learn Isolation Forest</em> machine learning engine, IMPOF accurately identifies the root cause of systemic latency spikes. Furthermore, IMPOF provides an empirical testing harness that allows DevOps engineers to systematically toggle optimization techniques across individual layers, calculate the <em>Optimization Gain Index (OGI)</em>, and objectively validate multi-tier architectural return on investment.
    </p>
  </div>
</div>

<!-- PAGE 10: CHAPTER 2 - LITERATURE SURVEY (Page 2) -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">2</div>
    <h2 class="chapter-title">CHAPTER-2</h2>
    <h3 class="section-title">2.1 LITERATURE SURVEY</h3>

    <p class="text-justify">
      Performance engineering and distributed tracing have been subjects of intensive investigation in computer science. Modern systems rely on tracing paradigms pioneered by Google's Dapper infrastructure and industry APM frameworks.
    </p>

    <p class="text-justify">
      <strong>1. Sigelman et al. (Google Dapper, 2010):</strong> Introduced the foundational architecture for large-scale distributed systems tracing. Dapper established that non-invasive span-context propagation (Trace ID and Span ID) provides end-to-end visibility across heterogeneous RPC services with less than 1.5% CPU overhead. IMPOF builds upon this concept by extending distributed tracing beyond backend microservices into client-side DOM rendering and database query spans [1].
    </p>

    <p class="text-justify">
      <strong>2. Liu, Ting, and Zhou (Isolation Forest, 2008):</strong> Developed the Isolation Forest algorithm for unsupervised anomaly detection. Unlike density- or distance-based anomaly detectors (such as Local Outlier Factor or One-Class SVM), Isolation Forest exploits the property that anomalies are few and structurally different, isolating them with shorter average path lengths in randomized trees. This research provides the theoretical foundation for IMPOF's automated ML anomaly detection engine [2].
    </p>

    <p class="text-justify">
      <strong>3. Dean and Barroso (The Tail at Scale, 2013):</strong> Demonstrated that high tail latency (P95, P99) severely damages user experience and resource utilization in large-scale online services. Their findings emphasize that simple average latency metrics disguise severe bottlenecking, necessitating granular percentiles and connection pooling mechanisms such as HikariCP to control queue latency. IMPOF directly implements P50, P90, P95, and P99 latency monitoring [3].
    </p>

    <p class="text-justify">
      <strong>4. Grigorik (High Performance Browser Networking, 2013):</strong> Examined transport-layer optimizations, proving that TCP slow start, round-trip time (RTT), and TLS negotiation overhead dominate web page load times. The study showed that Brotli/Gzip payload compression and HTTP/2 stream multiplexing reduce network transfer times by up to 85%. IMPOF incorporates these transport-layer controls into its optimization matrix [4].
    </p>
  </div>
</div>

<!-- PAGE 11: CHAPTER 2 - LITERATURE SURVEY (Page 3) -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">3</div>
    <p class="text-justify">
      <strong>5. Soundararajan et al. (Dynamic Database Optimization, 2009):</strong> Investigated database query execution plans, memory buffer pool allocation, and index selectivity. Their empirical work established that unindexed relational table scans scale linearly $O(N)$ with dataset size, causing thread pool starvation in upstream web servers. Incorporating B-Tree composite indices reduces search complexity to $O(\\log N)$, eliminating database-induced backpressure. IMPOF validates this through explicit SQL query profiling against 100,000+ relational records [5].
    </p>

    <p class="text-justify">
      <strong>6. Pedregosa et al. (Scikit-Learn Machine Learning in Python, 2011):</strong> Provided efficient, standardized implementations of state-of-the-art machine learning algorithms. The Scikit-Learn framework enables rapid deployment of ensemble and isolation tree methods within microservice environments. IMPOF utilizes Scikit-Learn within its Python FastAPI analytical core to provide low-latency inference on incoming telemetry vectors [6].
    </p>

    <p class="text-justify">
      <strong>7. Modern Observability and APM Survey (2020–2024):</strong> Recent comparative studies highlight that while commercial tools such as Datadog, Dynatrace, and New Relic excel at metrics collection, they operate as closed-source SaaS solutions with high egress costs and opaque machine learning algorithms. Modern DevOps teams require explainable, transparent root-cause analysis coupled with sandbox experimentation where optimizations can be verified before production rollout. IMPOF fills this research and tooling gap.
    </p>
  </div>
</div>

<!-- PAGE 12: CHAPTER 3 - EXISTING SYSTEM -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">4</div>
    <h2 class="chapter-title">CHAPTER-3</h2>
    <h3 class="section-title">3.1 EXISTING SYSTEM</h3>

    <p class="text-justify">
      In existing software production environments, performance monitoring and optimization are typically conducted using separate, disconnected tools:
    </p>

    <ul>
      <li><strong>Frontend Telemetry:</strong> Monitored using browser-based developer tools (Google Lighthouse) or client-side JavaScript error trackers (Sentry). These tools report Core Web Vitals but possess zero awareness of database query plans or backend worker queue depth.</li>
      <li><strong>Application Metrics:</strong> Collected via basic logging libraries (Winston, Log4j) or Prometheus metric scrapers that report raw HTTP request counts and memory footprints without cross-layer trace context.</li>
      <li><strong>Database Profiling:</strong> Handled by database administrators using slow query logs (`EXPLAIN ANALYZE`) in MySQL or PostgreSQL, completely isolated from HTTP request lifecycles.</li>
      <li><strong>Manual Ad-Hoc Optimization:</strong> Engineering teams hypothesize bottlenecks, deploy unverified code changes, and manually compare spreadsheet notes, leading to regressions and unpredictable production outcomes.</li>
    </ul>

    <h3 class="section-title">3.2 DISADVANTAGES</h3>
    <ol>
      <li><strong>Siloed Visibility and Metric Fragmentation:</strong> No unified timeline correlates a user's slow page click with the underlying microservice database scan.</li>
      <li><strong>Lack of Automated Cross-Layer Causal Correlation:</strong> Existing monitoring tools display charts side-by-side but fail to compute causal dependency chains across architectural tiers.</li>
      <li><strong>Black-Box AI Diagnostics:</strong> Enterprise APM tools deploy complex neural networks that flag alerts without explaining the underlying algorithmic criteria or domain logic.</li>
      <li><strong>Absence of Controlled Optimization Sandboxes:</strong> Current systems offer no native mechanism to toggle individual optimization techniques (e.g., caching vs. indexing vs. compression) and measure exact Before/After performance deltas.</li>
    </ol>
  </div>
</div>

<!-- PAGE 13: CHAPTER 3 - PROPOSED SYSTEM -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">5</div>
    <ol start="5">
      <li><strong>High Computational & Cost Overhead:</strong> Commercial APM agents inject substantial runtime overhead, frequently exceeding 10% CPU and incurring prohibitive telemetry transmission charges.</li>
      <li><strong>Inability to Prevent Tail Latency Cascades:</strong> Unpooled database connections and uncompressed payloads compound under high concurrency, causing sudden service failures that existing tools detect only after outages occur.</li>
    </ol>

    <h3 class="section-title">3.3 PROPOSED SYSTEM (IMPOF)</h3>
    <p class="text-justify">
      The proposed <strong>Integrated Multi-Layer Performance Optimization Framework (IMPOF)</strong> establishes a synchronized, full-stack performance engineering paradigm. The system architecture coordinates five interconnected layers through an end-to-end telemetry pipeline:
    </p>

    <ul>
      <li><strong>Multi-Layer Telemetry Ingestion:</strong> Non-invasive middleware captures spans across Frontend (Web Vitals), Network (payload bytes, compression ratios), Backend (event loop latency, CPU usage), Database (query execution times, scan rows), and Cache (hit/miss ratios).</li>
      <li><strong>Explainable Heuristic Bottleneck Classifier:</strong> A rule-based diagnostic engine scores each layer from 0 to 100 and classifies specific anti-patterns (e.g., Full Table Scans, N+1 Query Patterns, Thread Starvation, Uncompressed Network Payloads).</li>
      <li><strong>Machine Learning Anomaly Detection Core:</strong> An unsupervised <em>Isolation Forest</em> model trained on multidimensional metric vectors continuously flags operational anomalies with anomaly scores and confidence intervals.</li>
      <li><strong>Controlled Optimization Experiment Runner:</strong> An automated experimentation engine allows engineers to test four discrete optimization tiers: (1) Baseline Unoptimized, (2) Database Only, (3) Backend + DB, and (4) Full IMPOF (All 4 Layers), generating mathematical <em>Optimization Gain Index (OGI)</em> reports.</li>
    </ul>

    <h3 class="section-title">3.4 ADVANTAGES</h3>
    <ol>
      <li><strong>Comprehensive Cross-Layer Visibility:</strong> Visualizes end-to-end request lifecycles on a unified Gantt waterfall timeline.</li>
      <li><strong>Quantifiable Optimization Return on Investment:</strong> Calculates exact mathematical gain percentages for latency, throughput, and resource utilization.</li>
      <li><strong>Transparent, Explainable AI:</strong> Combines rule-based diagnostics with machine learning for transparent root-cause analysis.</li>
      <li><strong>Extensible Open-Source Architecture:</strong> Built on open standards (Node.js, FastAPI, PostgreSQL, Redis, React) with zero proprietary vendor lock-in.</li>
    </ol>
  </div>
</div>

<!-- PAGE 14: CHAPTER 4 - SYSTEM REQUIREMENTS -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">6</div>
    <h2 class="chapter-title">CHAPTER-4</h2>
    <h3 class="section-title">4.1 SYSTEM REQUIREMENTS</h3>
    <p class="text-justify">
      To execute, profile, and evaluate the Integrated Multi-Layer Performance Optimization Framework, the following hardware and software specifications are required.
    </p>

    <h4 class="subsection-title">4.1.1 H/W System Configuration:</h4>
    <ul>
      <li><strong>Processor:</strong> Intel Core i5 / AMD Ryzen 5 or higher (Quad-core minimum for concurrent load generation)</li>
      <li><strong>RAM:</strong> Minimum 8 GB (16 GB recommended for full multi-container Docker deployment)</li>
      <li><strong>Hard Disk:</strong> At least 20 GB free SSD storage space</li>
      <li><strong>Keyboard:</strong> Standard 104-key Windows Keyboard</li>
      <li><strong>Mouse:</strong> Optical Mouse / Trackpad</li>
      <li><strong>Monitor:</strong> High-Resolution 1920x1080 Full HD Display (for clear telemetry visualizations and waterfall charts)</li>
    </ul>

    <h3 class="section-title">4.2 SOFTWARE REQUIREMENTS:</h3>
    <ul>
      <li><strong>Operating System:</strong> Windows 10 / Windows 11 (or Linux Ubuntu 22.04 LTS / macOS 13+)</li>
      <li><strong>Backend Runtime:</strong> Node.js v18.0+ / v20.0+ with Express.js framework</li>
      <li><strong>Analysis Engine & ML Core:</strong> Python 3.10+ with FastAPI and Uvicorn ASGI server</li>
      <li><strong>Machine Learning Libraries:</strong> Scikit-Learn (Isolation Forest), NumPy, Pandas, Joblib</li>
      <li><strong>Database Systems:</strong> PostgreSQL 16 (Relational Audit Store) and MySQL 8.0 (Relational Benchmark DB)</li>
      <li><strong>Distributed In-Memory Cache:</strong> Redis 7.2 (Key-value store with TTL)</li>
      <li><strong>Frontend Web Framework:</strong> React 18, Vite build tool, JavaScript (ES6+), Vanilla CSS3</li>
      <li><strong>Containerization & Orchestration:</strong> Docker Engine 24+, Docker Compose v2.0+</li>
      <li><strong>Metrics Collection:</strong> Prometheus v2.50.0</li>
    </ul>
  </div>
</div>

<!-- PAGE 15: CHAPTER 5 - SYSTEM ARCHITECTURE -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">7</div>
    <h2 class="chapter-title">CHAPTER-5</h2>
    <h3 class="section-title">5.1 SYSTEM ARCHITECTURE</h3>

    <p class="text-justify">
      The architecture of the <strong>Integrated Multi-Layer Performance Optimization Framework (IMPOF)</strong> is structured as a decoupled, microservice-oriented ecosystem designed for high-resolution observability and multi-layer performance tuning. Figure 5.1 illustrates the structural interaction between the monitored application, ingestion pipelines, analytical intelligence cores, persistent datastores, and the DevOps React command center.
    </p>

    <div class="diagram-container">
      <div style="font-family: monospace; font-size: 8.5pt; text-align: left; line-height: 1.25; background: #fff; padding: 10px; border: 1px solid #ddd;">
<pre>
                      +-------------------------------------------------+
                      |          CLIENT BROWSER (React 18 Dashboard)    |
                      +-------------------------------------------------+
                                      |                       ^
                 HTTP Requests / Telemetry           WebSocket / REST Poll
                                      v                       |
+---------------------------------------------------------------------------------------+
|                              LAYER 2: NETWORK & TRANSPORT                             |
|       • Brotli / Gzip Payload Compression (-85%)     • HTTP/2 Multiplexed Streams     |
+---------------------------------------------------------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------------------+
|                    LAYER 3: CORE PLATFORM BACKEND (Node.js / Express)                 |
|       • JWT Authentication & Multi-Tenancy           • High-Resolution Timer Spans   |
|       • Controlled Experiment Runner                 • Metrics Ingestion Pipeline    |
+---------------------------------------------------------------------------------------+
              |                                       |                     |
              v                                       v                     v
+---------------------------+           +--------------------------+  +-----------------+
|   LAYER 4: DATABASE       |           |   LAYER 5: CACHE         |  | ANALYSIS ENGINE |
|   • PostgreSQL 16 Relational|         |   • Redis 7.2 Store      |  | (FastAPI/Python)|
|   • B-Tree Composite Index|           |   • In-Memory L1 LRU     |  | • Scikit-Learn  |
|   • HikariCP Connection   |           |   • TTL Invalidation     |  |   Isolation     |
|     Pool (Warm Leases)    |           |   • 99.9% Cache Hits     |  |   Forest ML     |
+---------------------------+           +--------------------------+  | • 0-100 Heuristic|
                                                                      |   Scorer        |
                                                                      +-----------------+
</pre>
      </div>
      <p style="font-weight: bold; font-size: 10.5pt; margin-top: 8px;">Fig-5.1: High-Level End-to-End System Architecture of IMPOF</p>
    </div>

    <p class="text-justify">
      Telemetry spans generated by client navigation APIs, backend middleware, database query listeners, and cache drivers are consolidated via the ingestion pipeline. The FastAPI analytical service evaluates health metrics and anomaly scores asynchronously, persisting results to PostgreSQL and Redis for real-time dashboard presentation.
    </p>
  </div>
</div>

<!-- PAGE 16: CHAPTER 6 - SYSTEM STUDY -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">8</div>
    <h2 class="chapter-title">CHAPTER-6</h2>
    <h3 class="section-title">6.1 SYSTEM STUDY</h3>

    <p class="text-justify">
      A comprehensive system study was conducted to analyze existing performance profiling workflows in modern enterprise software organizations. Modern DevOps teams struggle with fragmented tools that report high CPU utilization or slow page loads without identifying the root cause across upstream or downstream tiers. The objective of this study was to design an automated framework capable of non-invasively collecting metrics, decomposing total latency mathematically, scoring bottlenecks transparently, and empirically validating optimizations.
    </p>

    <h3 class="section-title">6.1.1 FEASIBILITY STUDY</h3>
    <p class="text-justify">
      A feasibility analysis was performed across economic, technical, and operational dimensions to verify that IMPOF can be practically built, deployed, and sustained.
    </p>

    <h4 class="subsection-title">6.1.1.a Economical Feasibility:</h4>
    <ul>
      <li><strong>Open-Source Technology Base:</strong> All core technologies—Node.js, Express, Python, FastAPI, Scikit-Learn, React, PostgreSQL, Redis, Docker, and Prometheus—are open-source under permissive MIT and Apache 2.0 licenses, eliminating expensive commercial licensing fees.</li>
      <li><strong>Zero Proprietary Cloud Lock-In:</strong> The system runs locally or in self-hosted Kubernetes clusters, avoiding costly vendor-managed APM per-host charges.</li>
      <li><strong>Substantial ROI:</strong> Optimizing system throughput by 23x directly decreases required cloud virtual machine capacity, yielding major cloud infrastructure cost reductions.</li>
    </ul>

    <h4 class="subsection-title">6.1.1.b Technical Feasibility:</h4>
    <ul>
      <li><strong>Proven Engineering Stack:</strong> Node.js provides non-blocking asynchronous I/O ideal for telemetry ingestion. Python FastAPI offers ultra-fast analytical compute for Scikit-Learn Isolation Forest machine learning models.</li>
      <li><strong>Lightweight Telemetry:</strong> High-resolution nanosecond timestamps (`process.hrtime.bigint()`) add negligible overhead (&lt;0.8% CPU).</li>
      <li><strong>Containerized Reproducibility:</strong> Docker Compose guarantees consistent runtime behavior across development, testing, and production environments.</li>
    </ul>

    <h4 class="subsection-title">6.1.1.c Operational Feasibility:</h4>
    <ul>
      <li><strong>User-Centric DevOps Dashboard:</strong> The React 18 frontend presents clear visual summaries, Gantt waterfalls, and plain-English recommendations.</li>
      <li><strong>Automated Experimentation:</strong> Engineers can test and verify optimizations with one click before committing code to production.</li>
    </ul>
  </div>
</div>

<!-- PAGE 17: CHAPTER 7 - SYSTEM DESIGN (Page 1) -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">9</div>
    <h2 class="chapter-title">CHAPTER-7</h2>
    <h3 class="section-title">7.1 SYSTEM DESIGN</h3>

    <p class="text-justify">
      System design defines the structural components, data models, communication interfaces, and runtime interactions of IMPOF. The design adheres to clean architectural separation between metric collection, data persistence, analytical intelligence, and presentation.
    </p>

    <h3 class="section-title">7.1.1 UML DIAGRAMS</h3>
    <p class="text-justify">
      Unified Modeling Language (UML) standardizes the visual representation of system architecture. The following diagrams specify the static structural and dynamic behavioral characteristics of IMPOF.
    </p>

    <h4 class="subsection-title">7.1.2 Class Diagram</h4>
    <p class="text-justify">
      The Class Diagram models the static object-oriented structure of the framework. It defines the core entity abstractions: `ApplicationRegistry`, `MetricsIngestor`, `BottleneckScorer`, `HealthScorer`, `IsolationForestDetector`, `ExperimentEngine`, and `TraceSpan`.
    </p>

    <div class="diagram-container">
      <div style="font-family: monospace; font-size: 8pt; text-align: left; line-height: 1.25; background: #fff; padding: 10px; border: 1px solid #ddd;">
<pre>
+------------------------------------+          +------------------------------------+
|         ApplicationRegistry        |          |           MetricsIngestor          |
+------------------------------------+          +------------------------------------+
| - appId: String                    |          | - buffer: List&lt;MetricPayload&gt;      |
| - appName: String                  | 1      * | - prometheusClient: Client         |
| - environment: String              |--------->+------------------------------------+
| - registeredAt: DateTime           |          | + ingest(payload: MetricPayload)   |
+------------------------------------+          | + flushToStorage(): Boolean        |
| + register(): Application          |          +------------------------------------+
| + getActiveApps(): List            |                            | 1
+------------------------------------+                            |
                                                                  v 1
+------------------------------------+          +------------------------------------+
|          BottleneckScorer          |          |       IsolationForestDetector      |
+------------------------------------+          +------------------------------------+
| - rules: Map&lt;String, RuleDefinition&gt;|         | - model: IsolationForest (sklearn) |
| - thresholds: Map&lt;String, Float&gt;   |          | - contamination: Float = 0.05      |
+------------------------------------+          +------------------------------------+
| + evaluate(metrics): BottleneckList|          | + train(dataset: Matrix): Void     |
| + calculateHealthScore(): Integer  |          | + detect(vector: Vector): Anomaly  |
+------------------------------------+          +------------------------------------+
</pre>
      </div>
      <p style="font-weight: bold; font-size: 10.5pt; margin-top: 8px;">Fig-7.1: UML Class Diagram for IMPOF Core Entities</p>
    </div>
  </div>
</div>

<!-- PAGE 18: CHAPTER 7 - SYSTEM DESIGN (Page 2) -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">10</div>
    <h4 class="subsection-title">7.1.3 Sequence Diagram</h4>
    <p class="text-justify">
      The Sequence Diagram illustrates the chronological message exchange between system components during an end-to-end request lifecycle and metric evaluation flow.
    </p>

    <div class="diagram-container">
      <div style="font-family: monospace; font-size: 8pt; text-align: left; line-height: 1.25; background: #fff; padding: 10px; border: 1px solid #ddd;">
<pre>
Client Browser        Express Gateway       Database/Cache       FastAPI Engine       PostgreSQL Store
      |                      |                     |                   |                     |
      |--- 1. HTTP Request ->|                     |                   |                     |
      |   (start hrtime)     |--- 2. Query / Get ->|                   |                     |
      |                      |<-- 3. Return Data --|                   |                     |
      |<-- 4. HTTP Response -|                     |                   |                     |
      |    (Span created)    |                                         |                     |
      |                      |--- 5. Dispatch Metrics Vector --------->|                     |
      |                      |                                         |-- 6. IsolationForest|
      |                      |                                         |-- 7. Heuristic Score|
      |                      |                                         |-- 8. Save Result -->|
      |<-- 9. Poll Live Telemetry & Waterfall Timeline --------------------------------------|
</pre>
      </div>
      <p style="font-weight: bold; font-size: 10.5pt; margin-top: 8px;">Fig-7.2: UML Sequence Diagram of Request Tracing & Anomaly Evaluation</p>
    </div>

    <h4 class="subsection-title">7.1.4 Activity Diagram</h4>
    <p class="text-justify">
      The Activity Diagram models the operational workflow executed when an engineer triggers an optimization experiment: selecting target architectural layers, executing stress tests, calculating the Optimization Gain Index (OGI), and persisting audit snapshots.
    </p>
  </div>
</div>

<!-- PAGE 19: CHAPTER 7 - SYSTEM DESIGN (Page 3: DFD) -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">11</div>
    <h4 class="subsection-title">7.1.5 Data Flow Diagram (DFD)</h4>
    <p class="text-justify">
      The Data Flow Diagram models how telemetry measurements pass through successive transformation processes from raw client/server emission to classified analytical reports.
    </p>

    <div class="diagram-container">
      <div style="font-family: monospace; font-size: 8pt; text-align: left; line-height: 1.25; background: #fff; padding: 10px; border: 1px solid #ddd;">
<pre>
[ EXTERNAL ENTITY ] ---> (1.0 Metric Ingestion Pipeline) ---> [ D1: Raw Spans Buffer ]
(Monitored App)                        |
                                       v
                        (2.0 Analytical Evaluation Core)
                        • Heuristic Bottleneck Rules
                        • Isolation Forest ML Inference
                                       |
                   +-------------------+-------------------+
                   |                                       |
                   v                                       v
         [ D2: PostgreSQL Store ]               (3.0 Visualization Engine)
         (Snapshots, Audits)                               |
                                                           v
                                                [ EXTERNAL ENTITY ]
                                                (DevOps Engineer Dashboard)
</pre>
      </div>
      <p style="font-weight: bold; font-size: 10.5pt; margin-top: 8px;">Fig-7.3: Data Flow Diagram (DFD Level 1) for IMPOF Telemetry Flow</p>
    </div>

    <h4 class="subsection-title">7.1.6 Component Diagram</h4>
    <p class="text-justify">
      The Component Diagram captures the physical packaging and wiring between software artifacts: React SPA Frontend, Express HTTP Gateway, Python FastAPI Analytical Service, PostgreSQL Database, Redis Cache, and Prometheus Scraper.
    </p>

    <h4 class="subsection-title">7.1.7 Use Case Diagram</h4>
    <p class="text-justify">
      Identifies the primary system actors (DevOps Engineer, Application Developer, System Administrator) and primary use cases: Register Application, Inspect Live Spans, Run Bottleneck Diagnosis, Launch Virtual Load Stress Test, and Export Audit Report.
    </p>
  </div>
</div>

<!-- PAGE 20: CHAPTER 7 - SYSTEM DESIGN (Page 4) -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">12</div>
    <h4 class="subsection-title">7.1.8 Deployment Diagram</h4>
    <p class="text-justify">
      The Deployment Diagram maps the deployment of software containers onto physical/virtual host hardware. All microservices communicate over an isolated Docker bridge network (`impof-network`) with dedicated volume mounts for PostgreSQL persistent storage.
    </p>

    <h4 class="subsection-title">7.1.9 Architectural Block Diagram</h4>
    <p class="text-justify">
      The functional architecture is divided into six coordinated blocks:
    </p>
    <ol>
      <li><strong>Presentation Layer:</strong> React 18 SPA with real-time SVG Gantt charts, Core Web Vitals telemetry cards, and multi-layer control matrices.</li>
      <li><strong>API Gateway & Ingestion Layer:</strong> Node.js/Express service receiving high-frequency metric payloads with non-blocking event loops.</li>
      <li><strong>Analytical Intelligence Core:</strong> Python FastAPI microservice executing rule-based heuristic scoring and Scikit-Learn Isolation Forest anomaly detection.</li>
      <li><strong>Experimentation & Load Engine:</strong> Configurable virtual-user load generator simulating 10 to 200 concurrent users with tail latency tracking.</li>
      <li><strong>Persistence & Cache Tier:</strong> PostgreSQL 16 relational database coupled with Redis 7.2 sub-millisecond in-memory cache.</li>
      <li><strong>Distributed Tracing Instrumentation:</strong> W3C TraceContext compliant span propagators with high-resolution nanosecond timers.</li>
    </ol>

    <h3 class="section-title">7.2 SOFTWARE ENVIRONMENT</h3>
    <p class="text-justify">
      The framework leverages standard, widely adopted modern technologies:
    </p>
    <ul>
      <li><strong>JavaScript / Node.js:</strong> Powers non-blocking server I/O and interactive client user interfaces.</li>
      <li><strong>Python:</strong> The undisputed standard for data engineering, scientific computing, and machine learning.</li>
      <li><strong>FastAPI:</strong> Modern, asynchronous ASGI web framework providing sub-millisecond JSON serialization and native OpenAPI validation.</li>
      <li><strong>Docker:</strong> Containerization platform ensuring cross-platform isolation and zero-configuration environment setup.</li>
    </ul>
  </div>
</div>

<!-- PAGE 21: CHAPTER 8 - IMPLEMENTATION -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">13</div>
    <h2 class="chapter-title">CHAPTER-8</h2>
    <h3 class="section-title">8.1 IMPLEMENTATION AND METHODOLOGY</h3>

    <p class="text-justify">
      The implementation of IMPOF follows a modular microservice architecture. The platform was built and validated using a dedicated benchmark application (Movie Recommendation System) managing 100,000+ relational entities.
    </p>

    <h3 class="section-title">8.2 MODULE DESCRIPTION</h3>
    <p class="text-justify">
      The framework comprises five functional modules:
    </p>

    <p class="text-justify">
      <strong>1. Metric Ingestion & Distributed Tracing Module:</strong> Intercepts incoming HTTP requests, binds unique `Trace-ID` and `Span-ID` tokens, and records nanosecond-accurate duration timestamps across route handlers, database queries, and cache lookups.
    </p>

    <p class="text-justify">
      <strong>2. Rule-Based Heuristic Bottleneck Scoring Module:</strong> Evaluates ingested metrics against deterministic thresholds. Computes layer health scores (0–100) and outputs structured diagnostic reasons (e.g., "Full Table Scan detected: query duration &gt; 100ms with zero index hits").
    </p>

    <p class="text-justify">
      <strong>3. Machine Learning Anomaly Detection Core:</strong> Employs an unsupervised <em>Isolation Forest</em> ensemble model. Analyzes six-dimensional telemetry feature vectors:
      <span class="formula-box" style="display: block; margin: 6px 0;">x = [CPU_util, Memory_MB, API_latency_ms, DB_latency_ms, Error_rate, Cache_hit_ratio]</span>
      Calculates anomaly scores between -1.0 (severe outlier) and +1.0 (normal operation).
    </p>

    <p class="text-justify">
      <strong>4. Controlled Optimization Experiment Engine:</strong> Manages comparative benchmark executions across four optimization presets: (1) Baseline Unoptimized, (2) Database Only, (3) Backend + DB, and (4) Full IMPOF (All 4 Layers).
    </p>

    <p class="text-justify">
      <strong>5. Interactive DevOps Command Center:</strong> React 18 single page dashboard displaying live waterfall traces, health breakdowns, anomaly cards, and exportable project documentation.
    </p>
  </div>
</div>

<!-- PAGE 22: CHAPTER 8 - MATHEMATICAL FORMULATIONS -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">14</div>
    <h3 class="section-title">8.3 ALGORITHMIC IMPLEMENTATION & MATHEMATICAL FORMULATIONS</h3>

    <p class="text-justify">
      The core analytical engine is governed by formal mathematical models:
    </p>

    <h4 class="subsection-title">1. Total Latency Decomposition:</h4>
    <div class="formula-box">
      T_total = T_client_render + T_network_rtt + T_backend_exec + T_database_query + T_queue_wait
    </div>
    <p class="text-justify">
      Where each constituent span is measured independently using monotonic high-resolution hardware timers.
    </p>

    <h4 class="subsection-title">2. Optimization Gain Index (OGI %):</h4>
    <div class="formula-box">
      OGI (%) = ((T_baseline - T_optimized) / T_baseline) * 100%
    </div>
    <p class="text-justify">
      OGI quantifies the percentage reduction in latency achieved by the optimization configuration relative to the unoptimized baseline.
    </p>

    <h4 class="subsection-title">3. Explainable Application Health Score:</h4>
    <div class="formula-box">
      HealthScore = 0.30*S_latency + 0.20*S_availability + 0.20*S_database + 0.15*S_cache + 0.15*S_infrastructure
    </div>
    <p class="text-justify">
      Each sub-score $S_i$ is mapped to a bounded range $[0, 100]$ using piecewise linear penalty functions.
    </p>

    <h4 class="subsection-title">4. Isolation Forest Anomaly Formulation:</h4>
    <div class="formula-box">
      s(x, n) = 2^(- ( E(h(x)) / c(n) ) )
    </div>
    <p class="text-justify">
      Where $h(x)$ represents the path length of observation $x$ in an isolation tree, $E(h(x))$ is the expectation across an ensemble of 100 trees, and $c(n)$ is the average path length of unsuccessful searches in a Binary Search Tree of $n$ samples:
    </p>
    <div class="formula-box">
      c(n) = 2*(ln(n - 1) + 0.5772156649) - (2*(n - 1) / n)
    </div>

    <h3 class="section-title">8.4 SYSTEM EXECUTION FLOW</h3>
    <ol>
      <li><strong>User Requests:</strong> Client initiates transactions or virtual load generator triggers concurrent requests.</li>
      <li><strong>Span Recording:</strong> Middlewares record timing markers at request entry, database dispatch, and response completion.</li>
      <li><strong>Metric Aggregation:</strong> Ingestion engine normalizes spans into feature vectors.</li>
      <li><strong>Inference & Scoring:</strong> FastAPI service executes heuristic rules and Isolation Forest anomaly inference.</li>
      <li><strong>Visualization:</strong> React dashboard updates waterfall graphs, health gauges, and anomaly badges in real time.</li>
    </ol>
  </div>
</div>

<!-- PAGE 23: CHAPTER 9 - SYSTEM TEST -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">15</div>
    <h2 class="chapter-title">CHAPTER-9</h2>
    <h3 class="section-title">9.1 SYSTEM TEST</h3>

    <p class="text-justify">
      Comprehensive testing of IMPOF was conducted to verify correctness, throughput scalability, error resilience, and predictive precision under heavy operational workloads.
    </p>

    <h3 class="section-title">9.2 TYPES OF TESTS</h3>
    <ul>
      <li><strong>Unit Testing:</strong> Tested isolated mathematical algorithms (OGI calculations, health scoring functions, Isolation Forest feature transformations).</li>
      <li><strong>Integration Testing:</strong> Verified communication channels between Node.js API gateway, FastAPI analysis engine, PostgreSQL database, and Redis cache.</li>
      <li><strong>Functional Testing:</strong> Validated user workflows: application registration, layer toggle controls, and benchmark execution.</li>
      <li><strong>System Testing:</strong> Executed end-to-end load simulations under 10 to 200 concurrent virtual users to verify thread stability and memory footprint.</li>
      <li><strong>White Box Testing:</strong> Inspected internal code paths, query execution plans, and memory leak profiles during sustained load.</li>
      <li><strong>Black Box Testing:</strong> Evaluated dashboard responsiveness and accuracy purely based on external inputs and rendered outputs.</li>
    </ul>

    <h3 class="section-title">9.3 TEST CASES AND VALIDATION MATRIX</h3>
    <table class="formal-table">
      <thead>
        <tr>
          <th style="width: 10%;">Test ID</th>
          <th style="width: 32%;">Input / Action</th>
          <th style="width: 45%;">Expected Output</th>
          <th style="width: 13%;">Result</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>TC01</strong></td>
          <td>Ingest valid 5-layer telemetry payload</td>
          <td>Return 200 OK, update metrics buffer, calculate health score</td>
          <td style="color: green; font-weight: bold; text-align: center;">PASS</td>
        </tr>
        <tr>
          <td><strong>TC02</strong></td>
          <td>Simulate slow query (&gt;500ms, full table scan)</td>
          <td>Heuristic engine flags Database Bottleneck with deduction</td>
          <td style="color: green; font-weight: bold; text-align: center;">PASS</td>
        </tr>
        <tr>
          <td><strong>TC03</strong></td>
          <td>Inject sudden CPU & latency anomaly</td>
          <td>Isolation Forest outputs anomaly score &lt; -0.2 with alert</td>
          <td style="color: green; font-weight: bold; text-align: center;">PASS</td>
        </tr>
        <tr>
          <td><strong>TC04</strong></td>
          <td>Run Before vs After Experiment</td>
          <td>Calculate accurate OGI %, latency delta, and throughput multiplier</td>
          <td style="color: green; font-weight: bold; text-align: center;">PASS</td>
        </tr>
        <tr>
          <td><strong>TC05</strong></td>
          <td>Concurrently simulate 50 virtual users</td>
          <td>System sustains execution without event loop block or crash</td>
          <td style="color: green; font-weight: bold; text-align: center;">PASS</td>
        </tr>
        <tr>
          <td><strong>TC06</strong></td>
          <td>Missing or malformed metric attributes</td>
          <td>Return 422 Unprocessable Entity with error message</td>
          <td style="color: green; font-weight: bold; text-align: center;">PASS</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- PAGE 24: CHAPTER 10 - RESULTS AND DISCUSSIONS (Page 1) -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">16</div>
    <h2 class="chapter-title">CHAPTER-10</h2>
    <h3 class="section-title">10.1 RESULTS AND DISCUSSIONS</h3>

    <p class="text-justify">
      The empirical evaluation of IMPOF was conducted on a live benchmark deployment consisting of a movie recommendation service handling 100,000+ relational items under varying levels of concurrency.
    </p>

    <h3 class="section-title">10.2 PERFORMANCE METRICS & EMPIRICAL EVALUATION MATRIX</h3>
    <p class="text-justify">
      Table 10.1 outlines the experimental results across the four progressive optimization configurations:
    </p>

    <table class="formal-table">
      <thead>
        <tr>
          <th>Metric / Parameter</th>
          <th>1. Baseline (Unoptimized)</th>
          <th>2. Database Only</th>
          <th>3. Backend + DB</th>
          <th>4. Full IMPOF (All 4 Layers)</th>
          <th>Overall Gain</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Total Response Time</strong></td>
          <td>181.8 ms</td>
          <td>158.1 ms</td>
          <td>170.8 ms</td>
          <td><strong>7.0 ms</strong></td>
          <td style="font-weight: bold; color: green;">+96.1% (OGI)</td>
        </tr>
        <tr>
          <td><strong>Database Query Latency</strong></td>
          <td>31.0 ms (Full Scan)</td>
          <td>0.06 ms (Indexed)</td>
          <td>0.06 ms (Indexed)</td>
          <td><strong>0.00 ms (Cached)</strong></td>
          <td style="font-weight: bold; color: green;">99.9% Faster</td>
        </tr>
        <tr>
          <td><strong>Network Payload Size</strong></td>
          <td>142.5 KB (Raw)</td>
          <td>142.5 KB (Raw)</td>
          <td>18.2 KB (Lean DTO)</td>
          <td><strong>3.8 KB (Brotli)</strong></td>
          <td style="font-weight: bold; color: green;">97.3% Smaller</td>
        </tr>
        <tr>
          <td><strong>Throughput (50 Concurrency)</strong></td>
          <td>24.2 RPS</td>
          <td>85.4 RPS</td>
          <td>180.0 RPS</td>
          <td><strong>555.6 RPS</strong></td>
          <td style="font-weight: bold; color: green;">23.0x Capacity</td>
        </tr>
        <tr>
          <td><strong>Largest Contentful Paint</strong></td>
          <td>2.8s (Poor)</td>
          <td>2.4s (Needs Imp.)</td>
          <td>1.5s (Good)</td>
          <td><strong>0.6s (Good)</strong></td>
          <td style="font-weight: bold; color: green;">4.6x Faster</td>
        </tr>
        <tr>
          <td><strong>Application Health Score</strong></td>
          <td>25 / 100 (Critical)</td>
          <td>58 / 100 (Fair)</td>
          <td>76 / 100 (Good)</td>
          <td><strong>94 / 100 (Healthy)</strong></td>
          <td style="font-weight: bold; color: green;">+69 Points</td>
        </tr>
      </tbody>
    </table>
    <p class="text-center" style="font-size: 10pt; font-weight: bold;">Table 10.1: Multi-Tier Empirical Benchmark Comparison</p>

    <h3 class="section-title">10.3 DISCUSSION OF RESULTS</h3>
    <p class="text-justify">
      The empirical results demonstrate the core hypothesis of this research: <em>systemic performance optimization is inherently non-linear and compound in nature</em>. Tuning the database layer alone reduced query latency from 31.0 ms to 0.06 ms, but total response time remained high (158.1 ms) due to uncompressed 142.5 KB payloads and frontend DOM rendering overhead. Only when all four architectural tiers were synchronized—combining DOM virtualization, Brotli compression, L1/L2 caching, lean DTO projections, and B-tree indexing—did latency plummet to 7.0 ms, delivering an extraordinary <strong>96.1% Optimization Gain Index</strong> and a <strong>23.0x throughput surge</strong>.
    </p>
  </div>
</div>

<!-- PAGE 25: CHAPTER 10 - LIMITATIONS & CHAPTER 11 - CONCLUSION -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">17</div>
    <h3 class="section-title">10.4 LIMITATIONS OF CURRENT SYSTEM</h3>
    <ul>
      <li><strong>Dependency on Synthetic Load Profiles:</strong> Current load simulations utilize predetermined concurrency models; organic unpredictable production traffic spikes may exhibit different tail latency distributions.</li>
      <li><strong>In-Memory Model Storage:</strong> The Isolation Forest model requires periodic re-training as operational traffic patterns evolve over seasonal timeframes.</li>
      <li><strong>Instrumentation Overhead under Ultra-High RPS:</strong> In scenarios exceeding 50,000 RPS, telemetry span serialization may require kernel-level eBPF instrumentation to prevent CPU contention.</li>
    </ul>

    <h2 class="chapter-title" style="margin-top: 30px;">CHAPTER-11</h2>
    <h3 class="section-title">11.1 CONCLUSION</h3>
    <p class="text-justify">
      The <strong>Integrated Multi-Layer Performance Optimization Framework (IMPOF)</strong> successfully demonstrates the transformative efficacy of holistic, cross-layer performance engineering for modern web systems. By transcending the limitations of isolated monitoring tools, IMPOF provides a unified, production-grade observability platform that correlates metrics across the frontend, network, backend, database, and cache.
    </p>

    <p class="text-justify">
      Key research milestones accomplished include:
    </p>
    <ul>
      <li>Development of a unified, high-resolution distributed tracing pipeline.</li>
      <li>Implementation of a transparent, rule-based 0–100 heuristic bottleneck classification engine.</li>
      <li>Integration of an unsupervised <em>Scikit-Learn Isolation Forest</em> machine learning model for automated anomaly detection.</li>
      <li>Empirical validation on 100,000+ relational items demonstrating a <strong>96.1% latency reduction</strong> and a <strong>23.0x throughput scaling</strong> factor.</li>
    </ul>

    <h3 class="section-title">11.2 FUTURE SCOPE</h3>
    <ul>
      <li><strong>Autonomous Auto-Remediation & Self-Healing:</strong> Integrating automatic database index creation, dynamic cache TTL tuning, and horizontal pod autoscaling based on ML anomaly triggers.</li>
      <li><strong>eBPF Kernel-Level Telemetry:</strong> Leveraging extended Berkeley Packet Filters to capture socket and I/O metrics directly from the Linux kernel with zero application runtime overhead.</li>
      <li><strong>Edge AI Anomaly Inference:</strong> Deploying quantized neural network models to edge CDN nodes for instantaneous distributed threat and bottleneck classification.</li>
    </ul>
  </div>
</div>

<!-- PAGE 26: CHAPTER 12 - REFERENCES -->
<div class="page">
  <div class="page-border-normal">
    <div class="page-num-top">18</div>
    <h2 class="chapter-title">CHAPTER-12</h2>
    <h3 class="section-title">12. REFERENCES / BIBLIOGRAPHY</h3>

    <div style="margin-top: 20px;">
      <p><strong>1. B. H. Sigelman et al. (Google Inc., 2010)</strong><br>
      <em>Title:</em> Dapper, a Large-Scale Distributed Systems Tracing Infrastructure<br>
      <em>Description:</em> Seminal paper establishing low-overhead distributed tracing principles, trace context propagation, and span tree representation for modern internet-scale distributed systems.</p>

      <p><strong>2. F. T. Liu, K. M. Ting, and Z. H. Zhou (IEEE ICDM, 2008)</strong><br>
      <em>Title:</em> Isolation Forest<br>
      <em>Description:</em> Theoretical foundation of the Isolation Forest algorithm, detailing randomized tree partitioning for linear-time unsupervised anomaly detection in multidimensional data.</p>

      <p><strong>3. J. Dean and L. A. Barroso (Communications of the ACM, 2013)</strong><br>
      <em>Title:</em> The Tail at Scale<br>
      <em>Description:</em> Examines the systemic impact of tail latency (P95, P99) in distributed systems and proposes software techniques to tolerate variability and prevent cascading service delays.</p>

      <p><strong>4. I. Grigorik (O'Reilly Media, 2013)</strong><br>
      <em>Title:</em> High Performance Browser Networking<br>
      <em>Description:</em> In-depth architectural analysis of TCP, TLS, HTTP/2 multiplexing, and compression algorithms (Gzip, Brotli) for optimizing web application transport latency.</p>

      <p><strong>5. G. Soundararajan, D. Lupei, S. Ghanbari, et al. (ACM SIGMOD, 2009)</strong><br>
      <em>Title:</em> Dynamic Resource Allocation and Query Optimization in Database Clusters<br>
      <em>Description:</em> Demonstrates the critical role of connection pooling, buffer cache tuning, and indexing in mitigating severe database server saturation.</p>

      <p><strong>6. F. Pedregosa et al. (Journal of Machine Learning Research, 2011)</strong><br>
      <em>Title:</em> Scikit-learn: Machine Learning in Python<br>
      <em>Description:</em> Comprehensive documentation of Python's foundational machine learning library, establishing implementations for Isolation Forests, regression, and clustering algorithms.</p>

      <p><strong>7. IEEE & ACM Software Engineering Conference Papers (2020–2025)</strong><br>
      <em>Title:</em> Cross-Layer Observability and Automated Root-Cause Diagnosis in Microservices<br>
      <em>Description:</em> Recent peer-reviewed studies examining the application of heuristic classification and distributed telemetry for full-stack web application performance optimization.</p>
    </div>
  </div>
</div>

</body>
</html>
"""

html_path = r"d:\Major project\crosslayer\docs\major_project_report.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML Report generated at: {html_path}")

# Now render to PDF using headless msedge or chrome
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

pdf_path = r"d:\Major project\crosslayer\docs\MAJOR_PROJECT_REPORT_IMPOF.pdf"
cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    html_path
]

print(f"Running command: {' '.join(cmd)}")
res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
if os.path.exists(pdf_path):
    print(f"Successfully generated PDF at: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
else:
    print("PDF generation failed:", res.stderr)
