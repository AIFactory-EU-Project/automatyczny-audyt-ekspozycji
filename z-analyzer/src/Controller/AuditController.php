<?php

namespace App\Controller;

use App\Entity\Camera;
use App\Entity\ReportPhotoAnalysis;
use App\Entity\Shop;
use App\Exception\ApiResponseException;
use App\Service\SegmentTranslator;
use App\Utility\DBAL\Type\SegmentType;
use App\Utility\Response\ApiResponse;
use FOS\RestBundle\Controller\Annotations as Rest;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Serializer\Tests\Normalizer\JsonSerializerNormalizer;

/**
 * @Route("/api/audit")
 */
class AuditController extends BaseController
{
    private SegmentTranslator $segmentTranslator;

    public function __construct(SegmentTranslator $segmentTranslator)
    {
        $this->segmentTranslator = $segmentTranslator;
    }

    /**
     * @Route("/{id}", name="audit_details", methods={"GET"})
     *
     * @param ReportPhotoAnalysis $audit
     *
     * @return ApiResponse
     * @throws ApiResponseException
     */
    public function auditDetails(ReportPhotoAnalysis $audit)
    {
        $auditRepo = $this->getDoctrine()->getRepository(ReportPhotoAnalysis::class);
        $auditDetails = $auditRepo->getReportDetails($audit);

        return $this->createApiResponse($auditDetails);
    }
}
