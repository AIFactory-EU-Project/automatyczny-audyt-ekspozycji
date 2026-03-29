<?php

namespace App\Service;

use App\Entity\Sku;
use Doctrine\ORM\EntityManagerInterface;

class SkuMapper
{
    private EntityManagerInterface $entityManager;

    public function __construct(
        EntityManagerInterface $entityManager
    ) {
        $this->entityManager = $entityManager;
    }

    /**
     * @param array $reportData
     * @return array
     */
    public function addSkuNameToReportData(array $reportData): array
    {
        $skuToFindArray = [];
        foreach ($reportData['boxes'] as $box) {
            $skuToFindArray[$box['skuIndex']] = $box['skuIndex'];
        }

        $skuRepository = $this->entityManager->getRepository(Sku::class);
        $skuArray = $skuRepository->getSkuListByIndex($skuToFindArray);

        $tempSkuArr = [];
        /** @var Sku $sku */
        foreach ($skuArray as $sku) {
            $tempSkuArr[$sku->getIndex()] = $sku->getName();
        }

        foreach ($reportData['boxes'] as &$box) {
            $box['skuName'] = $tempSkuArr[$box['skuIndex']];
        }

        return $reportData;
    }
}
