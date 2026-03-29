export type RequiredParams<T, K extends keyof T> = Partial<T> & Pick<T, K>;

export interface Order {
  column: string;
  order: OrderDirection;
}

export enum OrderDirection {
  DESC = 'desc',
  ASC = 'asc'
}
