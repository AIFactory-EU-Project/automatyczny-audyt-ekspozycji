<?php

namespace App\Normalizer\Shop;

use App\Entity\Shop;
use App\Service\AccuracyCalculator;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\Serializer\Normalizer\ContextAwareNormalizerInterface;
use Symfony\Component\Serializer\Normalizer\NormalizerInterface;

class ShopNormalizer implements ContextAwareNormalizerInterface
{
    private AccuracyCalculator $calculator;
    private EntityManagerInterface $em;

    public function __construct(AccuracyCalculator $accuracyCalculator, EntityManagerInterface $em)
    {
        $this->calculator = $accuracyCalculator;
        $this->em = $em;
    }

    /**
     * @param mixed $object
     * @param null $format
     * @param array $context
     * @return array|bool|float|int|string|void|null
     */
    public function normalize($object, $format = null, array $context = [])
    {
        return [
            'id' => $object->getId(),
            'name' => $object->getName(),
            'code' => $object->getCode(),
            'street' => $object->getStreet(),
            'zipCode' => $object->getZipCode(),
            'city' => $object->getCity(),
            'accuracy' => $this->calculator->calculateShopAccuracy($object),
        ];
    }

    /**
     * @param mixed $data
     * @param null $format
     * @param array $context
     * @return bool|void
     */
    public function supportsNormalization($data, $format = null, array $context = [])
    {
        return $data instanceof Shop;
    }
}
