<?php

namespace App\Service;

use Doctrine\ORM\EntityManagerInterface;
use HaydenPierce\ClassFinder\ClassFinder;

class NormalizerRetriever
{
    private AccuracyCalculator $acc;
    private EntityManagerInterface $em;

    public function __construct(AccuracyCalculator $acc, EntityManagerInterface $em)
    {
        $this->acc = $acc;
        $this->em = $em;
    }

    /**
     * @return array
     */
    public function getAllNormalizers(): array
    {
        try {
            $classList = ClassFinder::getClassesInNamespace(
                'App\Normalizer',
                ClassFinder::RECURSIVE_MODE
            );
        } catch (\Exception $e) {
            return [];
        }

        $objectList = [];
        foreach ($classList as $class) {
            $normalizerObject = new $class($this->acc, $this->em);
            $objectList[] = $normalizerObject;
        }

        return $objectList;
    }

    public function getContextualNormalizers($context)
    {
        // TODO: Normalizers grouped for controllers?
    }
}
