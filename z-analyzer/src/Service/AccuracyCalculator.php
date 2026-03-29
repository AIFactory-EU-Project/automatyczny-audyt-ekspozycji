<?php

namespace App\Service;

use App\Entity\ReportPhotoAnalysis;
use App\Entity\Shop;
use App\Utility\DBAL\Type\SegmentType;
use Doctrine\ORM\EntityManagerInterface;

class AccuracyCalculator
{
    private EntityManagerInterface $em;

    public function __construct(EntityManagerInterface $em)
    {
        $this->em = $em;
    }

    /**
     * @param Shop $shop
     * @return float|int
     */
    public function calculateShopAccuracy(Shop $shop)
    {
        // TODO real data! and caching?
        return null;

        $shopRepo = $this->em->getRepository(Shop::class);
        $quickSnackShopAudits = $shopRepo->getShopAudits($shop, SegmentType::QUICK_SNACK);
        $readyMealsShopAudits = $shopRepo->getShopAudits($shop, SegmentType::READY_MEAL);

        $shopScoreSum = 0;
        $auditCount = count($quickSnackShopAudits) + count($readyMealsShopAudits);

        if ($auditCount === 0) {
            return null;
        }

        foreach ($quickSnackShopAudits as $audit) {
            /** @var ReportPhotoAnalysis $report */
            $report = $this->em->getRepository(ReportPhotoAnalysis::class)->find($audit['id']);
            $shopScoreSum += $this->calculateAuditAccuracy($report);
        }

        foreach ($readyMealsShopAudits as $audit) {
            /** @var ReportPhotoAnalysis $report */
            $report = $this->em->getRepository(ReportPhotoAnalysis::class)->find($audit['id']);
            $shopScoreSum += $this->calculateAuditAccuracy($report);
        }

        return floor($shopScoreSum / $auditCount);
    }

    public function calculateAuditAccuracy(ReportPhotoAnalysis $photoAnalysis)
    {
        if ($this->getSegmentFromPhotoAnalysis($photoAnalysis) === SegmentType::GRILL) {
            return (int) $photoAnalysis->getData()['count'] ?: 0;
        }
        // TODO real data! and caching?

        return null;
        $boxes = $photoAnalysis->getData()['boxes'];

        $boxCount = count($boxes);

        if ($boxCount === 0) {
            return null;
        }

        $accuracySum = 0;
        foreach ($boxes as $box) {
            $accuracySum += $box['accuracy'];
        }

        return floor($accuracySum / $boxCount);
    }

    private function getSegmentFromPhotoAnalysis(ReportPhotoAnalysis $photoAnalysis): string
    {
        // TODO optimize by returning segment with sql
        return $photoAnalysis->getPhoto()->getCamera()->getSegment()->getType();
    }
}
