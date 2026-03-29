<?php
/**
 * @license AiFactory
 */

namespace App\Repository;

use App\Entity\AppLog;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Common\Persistence\ManagerRegistry;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;

/**
 * @method AppLog|null find($id, $lockMode = null, $lockVersion = null)
 * @method AppLog|null findOneBy(array $criteria, array $orderBy = null)
 * @method AppLog[]    findAll()
 * @method AppLog[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class AppLogRepository extends ServiceEntityRepository
{
    /**
     * AppLogRepository constructor.
     *
     * @param ManagerRegistry $registry
     */
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, AppLog::class);
    }

    /**
     * @param AppLog $logEntry
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function save(AppLog $logEntry)
    {
        $this->_em->persist($logEntry);
        $this->_em->flush();
    }
}
