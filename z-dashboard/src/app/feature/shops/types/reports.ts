import { ShopDetails } from '@app/feature/shops/types/shops';

export interface ReportBase {
  id: number,
  name: string,
  date: Date,
  accuracy: number,
  data?: {
    count: number;
    boxes:  ReportResult[];
  }
}

export interface Report extends ReportBase {
  segmentTypeName: string,
  shopId: number,
}

export interface ReportDetails {
  id: number;
  shop: ShopDetails;
  report: Omit<ReportBase, 'id'>;
  imageReal: ImageBox;
  imagePlanogram?: ImageBox;
  originalImage?: ImageBox;
  products?: ReportResult[];
  score?: number;
  count?: number;
}

export interface ImageBox {
  name: string,
  date: Date,
  url: string,
}

export interface ReportResult {
  shelf: number;
  position: number;
  index: string;
  skuName: string;
  faces_count: number;
  result: string;
  color: string;
  accuracy?: number;
  rect?: number[];
  status?: number;
}

export enum ReportType {
  READY_MEAL = 'Audyt Dań Gotowych',
  QUICK_SNACK = 'Audyt Szybkich Przekąsek',
  GRILL = 'Audyt Grillowy'
}
