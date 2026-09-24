## CrowdSense AI – Smart Crowd Management System

CrowdSense AI is an AI-powered crowd monitoring and management system designed to support safer and more organized large-scale events.

## Project Overview

Large events such as Hajj gatherings, stadium events, festivals, and crowded public spaces can experience high levels of crowd density, which may lead to congestion, restricted movement, and increased safety risks.
CrowdSense AI uses Computer Vision and crowd density estimation to analyze images, identify crowded areas, and provide organizers with information that can support better crowd management and decision-making.

## Problem

Large-scale events can face challenges such as:
High crowd density
Congestion in specific areas
Difficulty monitoring large spaces
Restricted movement
Difficulty identifying crowded zones quickly
Challenges in coordinating event staff

These challenges can affect the organization and safety of people within crowded environments.

## Solution

CrowdSense AI analyzes images  using Computer Vision and crowd density estimation.
The system divides the monitored area into four zones and estimates the crowd density in each zone.
Each zone is classified according to its crowd density level:
Low
Medium
High
Critical

This allows event organizers and supervisors to identify crowded areas and respond more effectively.

## How It Works

An image  is provided to the system.
YOLOv8 is used for person detection.
Crowd density is estimated using the Lightweight Crowd Counting (LWCC) approach.
The monitored area is divided into four zones.
The density level is calculated for each zone.
The system displays the crowd density information through the dashboard.
Organizers and supervisors can use the information to support crowd management decisions.

## System Roles

### Supervisor

The supervisor can monitor the overall event and review reports and crowd-related information.

### Organizer

The organizer can monitor assigned areas, review crowd conditions, and provide reports to the supervisor.

### Security Officer

The security officer can access relevant crowd information to support on-ground monitoring and response.
zones

## Technologies Used

### Artificial Intelligence & Computer Vision

Python
YOLOv8
Computer Vision
LWCC (Lightweight Crowd Counting)
OpenCV

## Backend

Flask

### Data & Processing
NumPy
Cv

### Frontend
HTML
CSS
JavaScript

## Model Training

The YOLOv8 model was trained using a crowd-related dataset to detect people in different environments.
The dataset was prepared and divided into training, validation, and testing sets before model training.

## Results

The trained YOLOv8 model achieved the following evaluation results:
Precision: 86.9%
Recall: 80.7%
mAP@50: 90.5%
mAP@50-95: 64.6%

## Use Cases
CrowdSense AI can support crowd monitoring in environments such as:

Hajj gatherings
Stadiums
Large events
Public markets
Festivals
Other crowded environments

## Project Goal
The goal of CrowdSense AI is to provide event organizers and supervisors with AI-powered information about crowd density and crowded zones, helping them monitor large spaces and support more organized crowd management.

## Disclaimer
CrowdSense AI is a decision-support and monitoring system. It is designed to assist event staff and does not replace human supervision or professional emergency and security procedures.
