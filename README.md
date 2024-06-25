# tugraph-course-resources

This is the course resources repository to learn tugraph projects.

This repository contains instructions to setup a TuGraph Docker container and code templates for 2 graph data mining tasks (the Louvain algorithm for community detection and the Node2Vec algorithm for link prediction). The code templates were originally used as programming assignments for AI3602 Data Mining at Shanghai Jiao Tong University.

## Files

- `assignment_releases/` contains the code templates for the programming assignments. The programming assignments are divided into 3 phases. Please refer to the `README.md` files under each directory for detailed directions for each phase.
  - `phase1_tugraph_setup/`. Phase 1 contains instructions on setting up a docker container for TuGraph and using TuGraph's Python API for development.
  - `phase2_louvain_community_detection/`. Phase 2 contains code templates for implementing the Louvain algorithm for community detection.
  - `phase3_node2vec_link_prediction/`. Phase 3 contains code templates for implementing the Node2Vec algorithm for link prediction.
- `autograding/` contains scripts for automated grading and code duplication detection (based on CodeBLEU scores).
- `zips/` contains zipped versions of the assignment releases= and autograding scripts. The contents in the zip files are identical with the code in this repository, and they are added for ease of downloading.
