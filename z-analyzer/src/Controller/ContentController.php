<?php

namespace App\Controller;

use App\Entity\ReportPhotoAnalysis;
use App\Entity\File;
use App\Exception\ApiResponseException;
use App\Utility\Response\ApiResponse;
use FOS\RestBundle\Controller\Annotations as Rest;
use Symfony\Component\HttpFoundation\BinaryFileResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

/**
 * @Route("/static-content")
 */
class ContentController extends BaseController
{
    /**
     * @Route("/{name}", name="content_serving", methods={"GET"})
     *
     * @param File $file
     *
     * @return ApiResponse
     * @throws ApiResponseException
     */
    public function contentServing(File $file)
    {
        return new BinaryFileResponse($file->getFullPath());
    }
}
