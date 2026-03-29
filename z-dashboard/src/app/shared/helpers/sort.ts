import { OrderDirection } from '@shared/types/common-type';

export const sortOrder: (order: boolean) => OrderDirection = (order: boolean) => {
  return order ? OrderDirection.ASC : OrderDirection.DESC;
};
