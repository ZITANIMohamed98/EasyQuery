export class ResponseQueryModel {
  user_id: string;
  activity_id: string;
  database_name: string;
  input: string;
  querypredicted: string;

  constructor(
    user_id: string = '',
    activity_id: string = '',
    database_name: string = 'default_db',
    input: string = '',
    querypredicted: string = 'SELECT * FROM table WHERE condition'
  ) {
    this.user_id = user_id;
    this.activity_id = activity_id;
    this.database_name = database_name;
    this.input = input;
    this.querypredicted = querypredicted;
  }
}