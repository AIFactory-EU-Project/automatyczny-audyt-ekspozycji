<?php

namespace App\Controller;

use App\Entity\Camera;
use App\Entity\ReportPhotoAnalysis;
use App\Entity\Shop;
use App\Exception\ApiResponseException;
use App\Service\AccuracyCalculator;
use App\Service\SegmentTranslator;
use App\Utility\DBAL\Type\SegmentType;
use App\Utility\Response\ApiResponse;
use FOS\RestBundle\Controller\Annotations as Rest;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Serializer\Tests\Normalizer\JsonSerializerNormalizer;

/**
 * @Route("/api/shop")
 */
class ShopController extends BaseController
{
    private SegmentTranslator $segmentTranslator;
    private AccuracyCalculator $accuracyCalculator;

    public function __construct(
        SegmentTranslator $segmentTranslator,
        AccuracyCalculator $accuracyCalculator
    ) {
        $this->segmentTranslator = $segmentTranslator;
        $this->accuracyCalculator = $accuracyCalculator;
    }

    /**
     * @Route("", name="shop_list", methods={"GET"})
     *
     * @return ApiResponse
     * @throws ApiResponseException
     */
    public function shopList()
    {
        $em = $this->getDoctrine()->getManager();
        $shopRepository = $em->getRepository(Shop::class);
        $shopList = $shopRepository->findAll();

        return $this->createApiResponse(
            $shopList,
            true,
            '',
            Response::HTTP_OK,
            []
        );
    }

    /**
     * @Route("/{id}")
     *
     * @param Shop $shop
     *
     * @return ApiResponse
     * @throws ApiResponseException
     */
    public function shopDetail(Shop $shop)
    {
        return $this->createApiResponse($shop);
    }

    /**
     * @Route("/{id}/{segmentType}", name="shop_audit_per_type_list", methods={"GET"})
     *
     * @param Shop $shop
     * @param string $segmentType
     *
     * @return ApiResponse
     * @throws ApiResponseException
     */
    public function auditListPerType(Shop $shop, $segmentType)
    {
        if (!array_key_exists($segmentType, SegmentType::$choices)) {
            return $this->createApiResponse(null, false, 'Wrong segment type');
        }

        $shopRepo = $this->getDoctrine()->getRepository(Shop::class);
        $auditListPerType = $shopRepo->getShopAudits($shop, $segmentType);
        foreach ($auditListPerType as &$audit) {
            /** @var ReportPhotoAnalysis $report */
            $report = $this->getDoctrine()->getRepository(ReportPhotoAnalysis::class)->find($audit['id']);
            $audit['accuracy'] = $this->accuracyCalculator->calculateAuditAccuracy($report);
        }
        return $this->createApiResponse($auditListPerType);
    }
}
