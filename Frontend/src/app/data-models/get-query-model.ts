export class GetQueryModel {
  user_id: string;
  activity_id: string;
  database_name: string;
  input: string;

  constructor(
    user_id: string = '',
    activity_id: string = '',
    database_name: string = 'default_db',
    input: string = ''
  ) {
    this.user_id = user_id;
    this.activity_id = activity_id;
    this.database_name = database_name;
    this.input = input;
  }
}