<?php

namespace App\Repository;

use App\Entity\Planogram;
use App\Entity\PlanogramElement;
use App\Entity\ReportPhotoAnalysis;
use App\Entity\Shop;
use App\Entity\Sku;
use App\Service\SkuMapper;
use App\Utility\DBAL\Type\SegmentType;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\DBAL\DBALException;
use Doctrine\Persistence\ManagerRegistry;
use Symfony\Component\DependencyInjection\ContainerInterface;
use Symfony\Component\Process\InputStream;
use Symfony\Component\Process\Process;

/**
 * @method ReportPhotoAnalysis|null find($id, $lockMode = null, $lockVersion = null)
 * @method ReportPhotoAnalysis|null findOneBy(array $criteria, array $orderBy = null)
 * @method ReportPhotoAnalysis[]    findAll()
 * @method ReportPhotoAnalysis[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class ReportPhotoAnalysisRepository extends ServiceEntityRepository
{
    private ContainerInterface $container;
    private SkuMapper $skuMapper;

    public function __construct(
        ManagerRegistry $registry,
        ContainerInterface $container,
        SkuMapper $skuMapper
    ) {
        parent::__construct($registry, ReportPhotoAnalysis::class);
        $this->container = $container;
        $this->skuMapper = $skuMapper;
    }

    /**
     * @param ReportPhotoAnalysis $report
     * @return array
     */
    public function getReportDetails(
        ReportPhotoAnalysis $report
    ): array {
        $camera = $report->getPhoto()->getCamera();
        $shop = $camera->getShop();

        $shortSegment = SegmentType::$shortChoices[$camera->getSegment()->getType()];

        $result = [];
        $result['shop'] = $this->getShopData($shop);


        $conn = $this->getEntityManager()->getConnection();
        try {
            $statementFile = $conn->prepare(
                $this->generateReportPhotoSql($report->getId())
            );
        } catch (DBALException $e) {
            $result['imageReal'] = false;
        }

        if ($statementFile->execute()) {
            $result['imageReal'] = $statementFile->fetch();
            $router = $this->container->get('router');
            $hostUrl = 'https://' . $router->getContext()->getHost();
            $result['imageReal']['url'] = $hostUrl . $result['imageReal']['url'];
        }

        try {
            $statementFile = $conn->prepare(
                $this->generateReportOriginalPhotoSql($report->getId())
            );
        } catch (DBALException $e) {
            $result['originalImage'] = false;
        }

        if ($statementFile->execute()) {
            $result['originalImage'] = $statementFile->fetch();
            $result['originalImage']['url'] = $hostUrl . $result['originalImage']['url'];
        }

        $reportName = $shortSegment .
            strtoupper(substr($shop->getCity(), 0, 3)) .
            $report->getDateTime()->format('Ymd');

        $result['report'] = [
            'name' => $reportName,
            'date' => $report->getDateTime()->format('Y-m-d H:i:s'),
        ];

        if ($camera->getSegment()->getType() === SegmentType::GRILL) {
            $result['count'] = (int) $report->getData()['count'] ?: 0;
            return $result;
        }


        $planogram = $report->getPlanogram();
        $planogramElements = $planogram->getPlanogramElements()->getValues();

        $jsonInput = [];
        $jsonInput['boxes'] = $report->getData()['boxes'];

        $skuList = [];
        /** @var PlanogramElement $element */
        foreach ($planogramElements as $element) {
            $jsonInput['planogram'][] = [
                'index' => (string) $element->getSku()->getIndex(),
                'shelf' => (int) $element->getShelf(),
                'position' => (int) $element->getPosition(),
                'faces_count' => (int) $element->getFacesCount()
            ];

            $skuList[$element->getSku()->getIndex()] = [
                'index' => $element->getSku()->getIndex(),
                'name' => $element->getSku()->getName(),
            ];
        }
        $encodedJson = json_encode($jsonInput);

        exec("/bin/echo '$encodedJson' | /usr/bin/python3 /usr/src/app/bin/generate_planogram_report.py", $output, $retVal);

        $data = json_decode($output[0], true);

        $planogramReportArr = $data['planogram_report'];

        foreach ($planogramReportArr as $key => $pyReport) {
            foreach ($jsonInput['boxes'] as $product) {
                if ($pyReport['index'] == $product['skuIndex']) {
                    $planogramReportArr[$key]['box'] = $product['box'];
                    $planogramReportArr[$key]['accuracy'] = $product['accuracy'];
                }
            }

            foreach ($skuList as $sku) {
                if ($pyReport['index'] == $sku['index']) {
                    $planogramReportArr[$key]['skuName'] = $sku['name'];
                }
            }
        }

        $result['abundance'] = $data['abundance'];
        $result['availability'] = $data['availability'];
        $result['products'] = $planogramReportArr;
        $result['score'] = $data['score'];

        return $result;
    }

    /**
     * @param Shop $shop
     * @return array
     */
    private function getShopData(Shop $shop): array
    {
        return [
            'id' => $shop->getId(),
            'code' => $shop->getCode(),
            'street' => $shop->getStreet(),
            'zipCode' => $shop->getZipCode(),
            'city' => $shop->getCity(),
        ];
    }

    /**
     * @param int $reportId
     * @param string $shortSegment
     * @param string $shopCity
     * @return string
     */
    private function generateReportSql(int $reportId, string $shortSegment, string $shopCity = "BRAKMIASTA"): string
    {
        return
            "
                SELECT
                    rpa.id as id,
                    CONCAT ('" . $shortSegment . "', UPPER(LEFT('" . $shopCity . "', 3)), TO_CHAR(rpa.date_time, 'YYYMMDDHH24MISS')) as name,
                    rpa.date_time as date,
                    rpa.data as data
                FROM report_photo_analysis rpa
                WHERE 
                    rpa.id = " . $reportId . "
            "
        ;
    }

    /**
     * @param int $reportId
     * @return string
     */
    private function generateReportPhotoSql(int $reportId): string
    {
        return
            "
                SELECT
                    f.name as name,
                    p.time as date,
                    CONCAT ('/static-content/', f.name) as url
                FROM report_photo_analysis rpa
                    LEFT JOIN photo p on rpa.photo_id = p.id
                    LEFT JOIN file f on p.storage_id::numeric = f.id
                WHERE
                    rpa.id = " . $reportId . ";
            ";
    }

    /**
     * @param int $reportId
     * @return string
     */
    private function generateReportOriginalPhotoSql(int $reportId): string
    {
        return
            "
                SELECT
                    f.name as name,
                    p.time as date,
                    CONCAT ('/static-content/', f.name) as url
                FROM report_photo_analysis rpa
                    LEFT JOIN photo p on rpa.real_photo_id = p.id
                    LEFT JOIN file f on p.storage_id::numeric = f.id
                WHERE
                    rpa.id = " . $reportId . ";
            ";
    }
}
