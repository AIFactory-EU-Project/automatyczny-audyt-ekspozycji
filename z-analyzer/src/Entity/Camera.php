<?php

namespace App\Entity;

use App\Utility\DataObject\ImageManipulationSettings;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Serializer\Encoder\JsonEncoder;
use Symfony\Component\Serializer\NameConverter\CamelCaseToSnakeCaseNameConverter;
use Symfony\Component\Serializer\Normalizer\ObjectNormalizer;
use Symfony\Component\Serializer\Serializer;

/**
 * @ORM\Entity(repositoryClass="App\Repository\CameraRepository")
 * @ORM\HasLifecycleCallbacks()
 */
class Camera
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue()
     * @ORM\Column(type="integer")
     */
    private $id;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $type;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\Segment", inversedBy="cameras")
     * @ORM\JoinColumn(name="segment_id", referencedColumnName="id")
     */
    private $segment;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\Shop", inversedBy="cameras")
     * @ORM\JoinColumn(name="shop_id", referencedColumnName="id")
     */
    private $shop;

    /**
     * @ORM\OneToMany(targetEntity="App\Entity\Photo", mappedBy="camera")
     */
    private $photos;

    /**
     * @ORM\Column(type="string", length=20)
     */
    private $ip;

    /**
     * @ORM\Column(type="text")
     */
    private $manipulationSettings;

    /**
     * @var Serializer
     */
    private $serializer;

    public function __construct()
    {
        $this->photos = new ArrayCollection();
        $this->manipulationSettings = new ImageManipulationSettings();
        if (!$this->serializer) {
            $normalizers = [
                new ObjectNormalizer(null, new CamelCaseToSnakeCaseNameConverter())
            ];
            $encoders = [new JsonEncoder()];
            $this->serializer = new Serializer($normalizers, $encoders);
        }
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getType(): ?string
    {
        return $this->type;
    }

    public function setType(string $type): self
    {
        $this->type = $type;

        return $this;
    }

    public function getSegment(): ?Segment
    {
        return $this->segment;
    }

    public function setSegment(Segment $segment): self
    {
        $this->segment = $segment;

        return $this;
    }

    public function getShop(): ?Shop
    {
        return $this->shop;
    }

    public function setShop(Shop $shop): self
    {
        $this->shop = $shop;

        return $this;
    }

    public function getPhotos(): Collection
    {
        return $this->photos;
    }

    public function getIp(): ?string
    {
        return $this->ip;
    }

    public function setIp(string $ip): self
    {
        $this->ip = $ip;

        return $this;
    }

    public function getManipulationSettings(): ImageManipulationSettings
    {
        /** @var ImageManipulationSettings $deserializedObject */
        $deserializedObject =  $this->serializer->deserialize(
            $this->manipulationSettings,
            ImageManipulationSettings::class,
            'json'
        );

        return $deserializedObject;
    }

    public function setManipulationSettings(ImageManipulationSettings $settings): self
    {
        $this->manipulationSettings = $this->serializer->serialize($settings, 'json');

        return $this;
    }

    /**
     * @ORM\PostLoad()
     */
    public function setSerializers()
    {
        $normalizers = [
            new ObjectNormalizer(null, new CamelCaseToSnakeCaseNameConverter())
        ];
        $encoders = [new JsonEncoder()];
        $this->serializer = new Serializer($normalizers, $encoders);
    }
}
