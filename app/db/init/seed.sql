CREATE EXTENSION IF NOT EXISTS pgcrypto;

INSERT INTO processingstage (stage_name, stage_description)
VALUES
  ('PARSING',   'Parsing of the task file.'),
  ('EXECUTION', 'Execution of the task logic.');

INSERT INTO processingstatus (status_name, status_description)
VALUES
  ('PENDING',     'The task is waiting to be processed.'),
  ('IN_PROGRESS', 'The task is being processed.'),
  ('COMPLETED',   'The task has been processed successfully.'),
  ('FAILED',      'The task processing has failed.');

INSERT INTO course (course_name, creation_timestamp)
VALUES ('Pruebas Automatizadas', CURRENT_TIMESTAMP);

INSERT INTO sysuser (email, password, creation_timestamp)
VALUES (
  'ca.escobar2434@uniandes.edu.co',
  crypt('password', gen_salt('bf')),
  CURRENT_TIMESTAMP
);

INSERT INTO courseuser (course_role, course_id, user_id)
VALUES ('professor', 1, 1);

INSERT INTO taskdefinition (definition_name, definition_description, creation_timestamp)
VALUES ('Cypress', 'Cypress parsing and execution', CURRENT_TIMESTAMP);

INSERT INTO stagebytaskdefinition (processing_stage_id, task_definition_id)
VALUES (1,1), (2,1);

INSERT INTO processingcontainer (
    container_name,
    container_description,
    remote_storage_path,
    run_command,
    creation_timestamp,
    task_definition_id,
    processing_stage_id
) VALUES
(
  'CYPRESS_PARSING_VALIDATION_202510',
  'Container for validating the parsing of Cypress tasks.',
  '/ftp/one/container/cypressParsing.tar.gz',
  'docker run --rm -v /mnt/data:/app/data cypress_parsing:latest python parse.py --config /app/config_parsing.json --validate',
  CURRENT_TIMESTAMP,
  1,
  1
),
(
  'CYPRESS_EXECUTION_VALIDATION_202510',
  'Container for validating the execution of Cypress tasks.',
  '/ftp/one/container/cypressExecution.tar.gz',
  'docker run --rm -v /mnt/data:/app/data cypress_execution:latest python execute.py --config /app/config_execution.json --run',
  CURRENT_TIMESTAMP,
  1,
  2
);
