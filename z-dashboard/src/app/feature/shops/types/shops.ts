import { RequiredParams } from '@shared/types/common-type';

export interface ShopBase {
  id: number;
  name: string;
  code: string;
}

export interface ShopAddress {
  street: string,
  zipCode: string,
  city: string
}

export interface ShopAgreement {
  accuracy: string
}

export type ShopList = RequiredParams<ShopBase, 'id' | 'name'> & ShopAddress & ShopAgreement;

export type ShopDetails = ShopBase & ShopAddress;

