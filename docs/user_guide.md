# ContinuityTracker User Guide

## Introduction

ContinuityTracker is a specialized media automation tool designed to identify and flag potential continuity errors across scenes in media productions. It helps editors and directors maintain narrative consistency by analyzing visual elements across different shots and scenes.

## Getting Started

### Accessing the Application

1. Navigate to the ContinuityTracker application URL or run it locally at http://localhost:5000
2. Log in with your credentials
3. If you don't have an account, click "Sign Up" to create one

### Creating a Project

1. From the dashboard, click "New Project"
2. Enter a project name and description
3. Configure project settings if needed
4. Click "Create Project"

## Uploading Media Assets

### Supported File Types

- Video: MP4, MOV
- Images: JPG, PNG

### Upload Process

1. Navigate to your project
2. Click "Upload Assets"
3. Drag and drop files or click to browse
4. For each asset, you can add metadata:
   - Scene number
   - Shot number
   - Timestamp
   - Custom tags

### Organizing Assets

1. Group assets by scene using the scene number field
2. Add tags to categorize assets
3. Use the search and filter functions to find specific assets

## Setting Up Continuity Rules

### Rule Types

- **Object Tracking**: Detect when objects appear, disappear, or change between scenes
- **Clothing**: Track costume consistency
- **Props**: Monitor prop placement and appearance
- **Lighting**: Identify lighting shifts
- **Time of Day**: Detect time inconsistencies

### Creating Rules

1. Go to "Rules" in your project
2. Click "New Rule"
3. Select the rule type
4. Configure parameters:
   - Priority (High, Medium, Low)
   - Description
   - Custom parameters specific to the rule type
5. Save the rule

## Running Analysis

### Analysis Options

1. Navigate to your project
2. Click "Run Analysis"
3. Select assets to include (or use all assets)
4. Select rules to apply
5. Configure notification settings
6. Click "Start Analysis"

### Analysis Process

1. The system uploads and processes the selected media assets
2. Gemini API analyzes visual elements across scenes
3. Continuity rules are applied to identify potential issues
4. Results are compiled and presented in the analysis report

## Reviewing Results

### Analysis Report

1. After analysis completes, view the report
2. The summary shows total issues found by severity and type
3. Each issue includes:
   - Type and description
   - Affected scenes and assets
   - Frame references
   - Confidence score
   - Suggested resolution

### Working with Issues

1. Click on an issue to see details
2. View side-by-side comparison of affected frames
3. Mark issues as:
   - Resolved
   - False positive
   - To be addressed
4. Add notes for your team

## Collaboration

### Sharing Projects

1. Go to project settings
2. Click "Manage Team"
3. Enter email addresses to invite team members
4. Set permissions (View, Edit, Admin)

### Notifications

1. Configure notification preferences in your account settings
2. Get alerts when:
   - Analysis completes
   - New issues are found
   - Team members comment on issues
   - Issues are resolved

## Exporting and Reporting

### Export Options

1. From the analysis report, click "Export"
2. Choose format:
   - PDF Report
   - CSV Data
   - JSON Data
3. Select what to include:
   - Summary only
   - All issues
   - Selected issues

### Integration with Other Tools

1. Use the API to integrate with editing software
2. Export markers directly to Adobe Premiere Pro
3. Generate frame lists for review

## Advanced Features

### Custom Rule Creation

1. Advanced users can create custom rules
2. Use the rule editor to define parameters
3. Create rule templates for future use

### Batch Processing

1. Upload multiple assets at once
2. Run analysis on multiple projects
3. Schedule automatic analysis for overnight processing

## Account Management

### Profile Settings

1. Update your name and contact information
2. Change password
3. Configure notification preferences
4. Connect third-party accounts

### Subscription Management

1. View current plan
2. Upgrade subscription
3. Manage billing information

## Troubleshooting

### Common Issues

1. **Upload Failures**
   - Check file size limits (max 5GB per file)
   - Verify file formats are supported
   - Ensure stable internet connection

2. **Analysis Errors**
   - Check that media assets are properly tagged
   - Verify rule configurations
   - Ensure Gemini API access is properly configured

3. **Performance Issues**
   - For large videos, try using lower resolution proxies
   - Break analysis into smaller batches
   - Check server resource utilization

### Getting Help

1. Check the knowledge base in the Help section
2. Contact support via email
3. Open an issue on GitHub for technical problems