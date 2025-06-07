export class ListAllowedDbModel {
  user_id: string;
  database_list: string[];

  constructor(user_id: string = '', database_list: string[] = []) {
    this.user_id = user_id;
    this.database_list = database_list;
  }
}